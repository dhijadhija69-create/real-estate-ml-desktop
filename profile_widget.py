"""
ui/profile_widget.py - User Profile Modal + Logout Button
"""

import os, csv, sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QDialog, QScrollArea, QFrame, QGraphicsDropShadowEffect,
    QLineEdit, QMessageBox
)
from PyQt6.QtCore  import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect, QByteArray
from PyQt6.QtGui   import QFont, QColor, QPainter, QLinearGradient, QPainterPath
from PyQt6.QtSvgWidgets import QSvgWidget

# ── Palette ───────────────────────────────────────────────────────────────────
G1     = "#6CB8A9"
G2     = "#1F5F5B"
BG     = "#F5F3EE"
CARD   = "#FFFFFF"
MUTED  = "#6b7f7e"
BORDER = "#d8e4e3"
ACCENT = "#1f8a85"


# ── Gradient Widget ───────────────────────────────────────────────────────────
class GradientWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        grad = QLinearGradient(0, 0, self.width(), self.height())
        grad.setColorAt(0, QColor(G1))
        grad.setColorAt(1, QColor(G2))
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 18, 18)
        painter.fillPath(path, grad)


# ── Avatar Chip ───────────────────────────────────────────────────────────────
class AvatarChip(QPushButton):
    def __init__(self, username: str, parent=None):
        super().__init__(parent)
        self.setText(f"  {username[:1].upper()}  {username}")
        self.setFixedHeight(44)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.18);
                border: 1.5px solid rgba(255,255,255,0.35);
                color: white; border-radius: 22px;
                padding: 0 16px; font-size: 13px; font-weight: 600;
            }
            QPushButton:hover { background: rgba(255,255,255,0.28); }
        """)


# ── Logout Button ─────────────────────────────────────────────────────────────
class LogoutButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("  Log out", parent)
        self.setFixedHeight(44)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._apply_style(False)

    def _apply_style(self, hovered):
        self.setStyleSheet("""
            QPushButton {
                background: rgba(255,80,80,0.22);
                border: 1.5px solid rgba(255,150,150,0.45);
                color: #ffe0e0; border-radius: 12px;
                padding: 0 14px; font-size: 13px; font-weight: 500;
            }
        """ if hovered else """
            QPushButton {
                background: rgba(255,255,255,0.10);
                border: 1.5px solid rgba(255,255,255,0.30);
                color: white; border-radius: 12px;
                padding: 0 14px; font-size: 13px; font-weight: 500;
            }
        """)

    def enterEvent(self, e): self._apply_style(True);  super().enterEvent(e)
    def leaveEvent(self, e): self._apply_style(False); super().leaveEvent(e)


# ── Header Bar ────────────────────────────────────────────────────────────────
class HeaderBar(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self, user: dict, parent=None):
        super().__init__(parent)
        self.user = user
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        self.avatar_btn = AvatarChip(user.get("username", "User"))
        self.avatar_btn.clicked.connect(self._open_profile)
        self.logout_btn = LogoutButton()
        self.logout_btn.clicked.connect(self._confirm_logout)
        layout.addWidget(self.avatar_btn)
        layout.addWidget(self.logout_btn)

    def _open_profile(self):
        ProfileModal(self.user, parent=self.window()).exec()

    def _confirm_logout(self):
        msg = QMessageBox(self.window())
        msg.setWindowTitle("Log out")
        msg.setText("Are you sure you want to log out?")
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
        msg.setDefaultButton(QMessageBox.StandardButton.Cancel)
        msg.setStyleSheet("""
            QMessageBox { background: #F5F3EE; }
            QLabel { color: #1a2e2d; font-size: 14px; }
            QPushButton {
                background: #1F5F5B; color: white; border-radius: 8px;
                padding: 8px 20px; font-size: 13px; font-weight: 600; min-width: 80px;
            }
            QPushButton:hover { background: #6CB8A9; }
        """)
        if msg.exec() == QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()


# ── CSV Path Finder ───────────────────────────────────────────────────────────
def _find_predictions_csv() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(here, "..", "data", "predictions.csv"),
        os.path.join(os.getcwd(), "data", "predictions.csv"),
    ]
    if sys.argv:
        candidates.append(os.path.join(
            os.path.dirname(os.path.abspath(sys.argv[0])), "data", "predictions.csv"))
    for p in candidates:
        n = os.path.normpath(p)
        if os.path.isfile(n):
            return n
    return os.path.normpath(candidates[0])


# ── Prediction Loader ─────────────────────────────────────────────────────────
def _load_user_predictions(email: str, max_rows: int = 50) -> list[dict]:
    csv_path = _find_predictions_csv()
    if not os.path.isfile(csv_path):
        print(f"[DarPredict] CSV introuvable : {csv_path}")
        return []
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("user_email", "").strip() == email.strip():
                rows.append(row)
    print(f"[DarPredict] {len(rows)} prédictions pour '{email}' -> {csv_path}")
    return list(reversed(rows))[:max_rows]


# ── SVG Icon ──────────────────────────────────────────────────────────────────
def _make_svg_icon(icon_type: str) -> QSvgWidget:
    svgs = {
        "user": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
             stroke="#1f8a85" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
          <circle cx="12" cy="7" r="4"/></svg>""",
        "email": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
             stroke="#1f8a85" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="2" y="4" width="20" height="16" rx="2"/>
          <polyline points="2,4 12,13 22,4"/></svg>""",
    }
    icon = QSvgWidget()
    icon.load(QByteArray(svgs.get(icon_type, svgs["email"]).encode()))
    icon.setFixedSize(24, 24)
    icon.setStyleSheet("background: transparent;")
    return icon


# ── Section Title ─────────────────────────────────────────────────────────────
def _section_title(text: str, badge: str = "") -> QWidget:
    w = QWidget(); w.setStyleSheet("background: transparent;")
    row = QHBoxLayout(w)
    row.setContentsMargins(0, 4, 0, 4); row.setSpacing(8)
    lbl = QLabel(text)
    lbl.setStyleSheet(
        "color:#2d2d2d; font-size:14px; font-weight:700; background:transparent;")
    row.addWidget(lbl)
    if badge:
        b = QLabel(badge)
        b.setStyleSheet(f"""
            background:{G1}; color:white; font-size:11px; font-weight:700;
            padding:2px 10px; border-radius:10px;
        """)
        row.addWidget(b)
    row.addStretch()
    return w


# ── Info Tile (beige card used inside prediction card) ────────────────────────
def _info_tile(label: str, value: str, emoji: str = "") -> QWidget:
    w = QWidget()
    w.setStyleSheet(f"background:{BG}; border-radius:12px; border:1px solid {BORDER};")
    col = QVBoxLayout(w)
    col.setContentsMargins(14, 10, 14, 10); col.setSpacing(3)

    lbl_w = QLabel(label)
    lbl_w.setStyleSheet(
        f"color:{ACCENT}; font-size:11px; font-weight:500; background:transparent;")

    val_text = f"{emoji}  {value}" if emoji else value
    val_w = QLabel(val_text)
    val_w.setStyleSheet(
        "color:#1a2e2d; font-size:14px; font-weight:700; background:transparent;")

    col.addWidget(lbl_w); col.addWidget(val_w)
    return w


# ── Stats Banner ──────────────────────────────────────────────────────────────
def _stats_banner(predictions: list[dict]) -> QWidget:
    banner = GradientWidget(); banner.setFixedHeight(82)
    layout = QHBoxLayout(banner)
    layout.setContentsMargins(24, 0, 24, 0); layout.setSpacing(0)

    prices = []
    for p in predictions:
        try: prices.append(int(float(p.get("prix_predit_DH", 0))))
        except Exception: pass

    avg = int(sum(prices) / len(prices)) if prices else 0
    mx  = max(prices) if prices else 0

    def block(label, val):
        bw = QWidget(); bw.setStyleSheet("background:transparent;")
        c = QVBoxLayout(bw); c.setSpacing(1); c.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v = QLabel(val)
        v.setStyleSheet(
            "color:white; font-size:16px; font-weight:800; background:transparent;")
        v.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l = QLabel(label)
        l.setStyleSheet(
            "color:rgba(255,255,255,0.70); font-size:10px; background:transparent;")
        l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        c.addWidget(v); c.addWidget(l); return bw

    def vline():
        f = QFrame(); f.setFrameShape(QFrame.Shape.VLine)
        f.setStyleSheet("color:rgba(255,255,255,0.25);"); return f

    fmt = lambda n: f"{n:,}".replace(",", ".") + " DH" if n else "—"
    layout.addWidget(block("Prédictions", str(len(predictions))))
    layout.addWidget(vline())
    layout.addWidget(block("Prix moyen", fmt(avg)))
    layout.addWidget(vline())
    layout.addWidget(block("Prix max", fmt(mx)))
    return banner


# ── Helper ────────────────────────────────────────────────────────────────────
def _int_val(v) -> int:
    try: return int(v)
    except Exception: return 0


# ── Prediction Card ───────────────────────────────────────────────────────────
def _prediction_card(row: dict) -> QWidget:
    FEATURES = [
        ("🏊", "Piscine",    "piscine"),
        ("🚗", "Garage",     "garage"),
        ("🌱", "Balcon",     "balcon"),
        ("☀️",  "Terrasse",  "terrasse"),
        ("🅿️",  "Parking",   "parking"),
        ("🧑‍🌾", "Gardien",   "gardien"),
        ("🛗",  "Ascenseur", "ascenseur"),
        ("🌳",  "Jardin",    "jardin"),
        ("🌅",  "Belle Vue", "belle_vue"),
    ]

    card = QWidget()
    card.setStyleSheet(f"""
        QWidget {{ background:white; border-radius:18px; border:1.5px solid {BORDER}; }}
    """)
    sh = QGraphicsDropShadowEffect()
    sh.setBlurRadius(20); sh.setColor(QColor(31, 95, 91, 25)); sh.setOffset(0, 5)
    card.setGraphicsEffect(sh)

    layout = QVBoxLayout(card)
    layout.setContentsMargins(18, 16, 18, 16)
    layout.setSpacing(10)

    # ── Row 1: date + price ───────────────────────────────────────
    top = QHBoxLayout()

    date_str = row.get("date", "")
    try:
        from datetime import datetime
        dt = datetime.strptime(date_str[:19], "%Y-%m-%d %H:%M:%S")
        date_fmt = dt.strftime("%d %b %Y  à  %H:%M")
    except Exception:
        date_fmt = date_str[:16] or "—"

    date_lbl = QLabel(f"📅  {date_fmt}")
    date_lbl.setStyleSheet(
        f"color:{MUTED}; font-size:12px; background:transparent; border:none;")

    price_raw = row.get("prix_predit_DH", "0")
    try:    price_fmt = f"{int(float(price_raw)):,}".replace(",", ".") + " DH"
    except: price_fmt = f"{price_raw} DH"

    price_lbl = QLabel(f"$  {price_fmt}")
    price_lbl.setStyleSheet(f"""
        background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 {G1},stop:1 {G2});
        color:white; font-size:13px; font-weight:800;
        padding:6px 18px; border-radius:16px; border:none;
    """)

    top.addWidget(date_lbl); top.addStretch(); top.addWidget(price_lbl)
    layout.addLayout(top)

    # ── Divider ───────────────────────────────────────────────────
    div = QFrame(); div.setFrameShape(QFrame.Shape.HLine)
    div.setStyleSheet(f"background:{BORDER}; border:none;"); div.setFixedHeight(1)
    layout.addWidget(div)

    # ── Row 2: Surface + Rooms ────────────────────────────────────
    r2 = QHBoxLayout(); r2.setSpacing(10)
    surface   = row.get("surface", "?")
    chambres  = row.get("chambres", "?")
    sdb       = row.get("salles_de_bain", "?")
    r2.addWidget(_info_tile("Surface", f"{surface} m²"))
    r2.addWidget(_info_tile("Rooms",   f"{chambres} bed  •  {sdb} bath"))
    layout.addLayout(r2)

    # ── Row 3: Location (full width) ─────────────────────────────
    localisation = row.get("localisation", "?")
    quartier     = row.get("quartier", "").strip()
    loc_val      = (f"{localisation}, {quartier}"
                    if quartier and quartier not in ("", "N/A", "?")
                    else localisation)
    layout.addWidget(_info_tile("Localisation", loc_val, "📍"))

    # ── Row 4: Étage + Année + Cuisine ───────────────────────────
    r4 = QHBoxLayout(); r4.setSpacing(10)
    etage = row.get("etage", "?")
    annee = row.get("annee", "?")
    kitchen_rev = {0: "Basic", 1: "Modern", 2: "Luxury"}
    try:    k_name = kitchen_rev.get(int(float(row.get("kitchen", 0))), "Basic")
    except: k_name = str(row.get("kitchen", "—"))
    r4.addWidget(_info_tile("Étage",   str(etage), "⬡"))
    r4.addWidget(_info_tile("Année",   str(annee), "📅"))
    r4.addWidget(_info_tile("Cuisine", k_name,     "🍳"))
    layout.addLayout(r4)

    # ── Row 5: Feature chips (active only) ───────────────────────
    active = [(e, lbl) for e, lbl, key in FEATURES
              if _int_val(row.get(key, 0)) == 1]
    if active:
        cw = QWidget(); cw.setStyleSheet("background:transparent;")
        cl = QHBoxLayout(cw)
        cl.setContentsMargins(0, 0, 0, 0); cl.setSpacing(6)
        for emoji, lbl in active:
            chip = QLabel(f"{emoji} {lbl}")
            chip.setStyleSheet(f"""
                background:{G1}; color:white; font-size:11px; font-weight:600;
                padding:3px 10px; border-radius:10px;
            """)
            cl.addWidget(chip)
        cl.addStretch()
        layout.addWidget(cw)

    return card


# ── Profile Modal ─────────────────────────────────────────────────────────────
class ProfileModal(QDialog):

    def __init__(self, user: dict, parent=None):
        super().__init__(parent)
        self.user = user
        self.setWindowTitle("User Profile")
        self.setFixedWidth(500)
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._username_edit = None
        self._email_edit    = None
        self._build_ui()
        self._center_on_parent()
        self._animate_in()

    def _center_on_parent(self):
        if self.parent():
            pg = self.parent().geometry()
            self.move(
                pg.x() + (pg.width()  - self.width()) // 2,
                pg.y() + (pg.height() - 680)           // 2,
            )

    def _animate_in(self):
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(220)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        g = self.geometry()
        self.anim.setStartValue(QRect(g.x(), g.y() + 20, g.width(), g.height()))
        self.anim.setEndValue(g)
        self.anim.start()

    def _save_all(self):
        new_username = self._username_edit.text().strip()
        new_email    = self._email_edit.text().strip()
        if not new_username or not new_email:
            QMessageBox.warning(self, "Erreur", "Le nom et l'email ne peuvent pas être vides !")
            return

        old_email = self.user.get("email", "")
        self.user["username"] = new_username
        self.user["email"]    = new_email

        base = os.path.join(os.path.dirname(__file__), "..", "data", "users.csv")
        if os.path.isfile(base):
            rows, fieldnames = [], []
            with open(base, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames or []
                for r in reader:
                    if r.get("email") == old_email:
                        r["username"] = new_username
                        r["email"]    = new_email
                    rows.append(r)
            with open(base, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader(); writer.writerows(rows)

        QMessageBox.information(self, "Sauvegardé", "✅  Modifications enregistrées !")

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        container.setObjectName("profileContainer")
        container.setStyleSheet(f"""
            #profileContainer {{
                background:{CARD}; border-radius:22px; border:1px solid {BORDER};
            }}
        """)
        sh = QGraphicsDropShadowEffect()
        sh.setBlurRadius(40); sh.setColor(QColor(31, 95, 91, 60)); sh.setOffset(0, 12)
        container.setGraphicsEffect(sh)

        v = QVBoxLayout(container)
        v.setContentsMargins(0, 0, 0, 0); v.setSpacing(0)

        # Gradient header
        header = GradientWidget(); header.setFixedHeight(160)
        hl = QVBoxLayout(header)
        hl.setContentsMargins(28, 16, 20, 24); hl.setSpacing(0)

        close_btn = QPushButton("×")
        close_btn.setFixedSize(36, 36)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background:rgba(0,0,0,0.28); border:none; border-radius:18px;
                color:white; font-size:22px; font-weight:300;
            }
            QPushButton:hover { background:rgba(0,0,0,0.45); }
        """)
        close_btn.clicked.connect(self.close)
        cr = QHBoxLayout(); cr.addStretch(); cr.addWidget(close_btn)
        hl.addLayout(cr)

        username = self.user.get("username", "U")
        avatar = QLabel(username[:1].upper())
        avatar.setFixedSize(80, 80)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setFont(QFont("Segoe UI", 30, QFont.Weight.Bold))
        avatar.setStyleSheet(
            "background:white; border:none; border-radius:40px; color:#1f5f5b;")

        tc = QVBoxLayout(); tc.setSpacing(4)
        tc.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        t1 = QLabel("User Profile")
        t1.setStyleSheet(
            "color:white; font-size:22px; font-weight:700; background:transparent;")
        t2 = QLabel("View your information and prediction history")
        t2.setWordWrap(True)
        t2.setStyleSheet(
            "color:rgba(255,255,255,0.80); font-size:13px; background:transparent;")
        tc.addWidget(t1); tc.addWidget(t2)

        ir = QHBoxLayout(); ir.setSpacing(18); ir.setContentsMargins(0, 10, 0, 0)
        ir.addWidget(avatar); ir.addLayout(tc); ir.addStretch()
        hl.addLayout(ir)
        v.addWidget(header)

        # Scroll body
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background:transparent;")

        body = QWidget(); body.setStyleSheet("background:#f5f5f0;")
        bl = QVBoxLayout(body)
        bl.setContentsMargins(20, 20, 20, 24); bl.setSpacing(10)

        # Personal info section
        bl.addWidget(_section_title("👤  Personal Information"))
        bl.addWidget(self._editable_row("user",  "Username",      username))
        bl.addWidget(self._editable_row("email", "Email Address", self.user.get("email", "—")))

        save_btn = QPushButton("💾  Save Changes")
        save_btn.setFixedHeight(46)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 {G1},stop:1 {G2});
                color:white; border:none; border-radius:12px;
                font-size:14px; font-weight:700;
            }}
            QPushButton:hover {{ background:{G2}; }}
        """)
        save_btn.clicked.connect(self._save_all)
        bl.addWidget(save_btn)

        # Prediction history section
        bl.addSpacing(6)
        email       = self.user.get("email", "")
        predictions = _load_user_predictions(email)
        badge       = f"({len(predictions)} prédictions)" if predictions else ""
        bl.addWidget(_section_title("🕐  Prediction History", badge))

        if predictions:
            bl.addWidget(_stats_banner(predictions))
            bl.addSpacing(4)
            for pred in predictions:
                bl.addWidget(_prediction_card(pred))
        else:
            csv_path = _find_predictions_csv()
            exists   = os.path.isfile(csv_path)
            msg_text = (
                "Aucune prédiction trouvée.\n\n"
                f"Email : {email}\n"
                f"CSV : {'✅ trouvé' if exists else '❌ introuvable'}\n"
                f"{csv_path}"
            )
            empty = QLabel(msg_text)
            empty.setWordWrap(True)
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet("""
                color:#888; font-size:12px; background:white;
                border-radius:12px; border:1px solid #e8e8e0; padding:20px;
            """)
            bl.addWidget(empty)

        bl.addStretch()
        scroll.setWidget(body)
        scroll.setFixedHeight(500)
        v.addWidget(scroll)
        outer.addWidget(container)

    def _editable_row(self, icon_type: str, label: str, value: str) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background:white; border-radius:12px; border:1px solid #e8e8e0;")
        w.setMinimumHeight(68)
        h = QHBoxLayout(w)
        h.setContentsMargins(16, 12, 16, 12); h.setSpacing(14)
        h.addWidget(_make_svg_icon(icon_type))
        col = QVBoxLayout(); col.setSpacing(3)
        lbl_w = QLabel(label)
        lbl_w.setStyleSheet(
            f"color:{ACCENT}; font-size:11px; font-weight:500; background:transparent;")
        edit = QLineEdit(value)
        edit.setStyleSheet("""
            color:#1a1a1a; font-size:14px; font-weight:600;
            background:transparent; border:none;
            border-bottom:1.5px solid #d0e8e6; padding:2px 0;
        """)
        col.addWidget(lbl_w); col.addWidget(edit)
        h.addLayout(col); h.addStretch()
        if icon_type == "user": self._username_edit = edit
        else:                   self._email_edit    = edit
        return w

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event):
        if hasattr(self, "_drag_pos") and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
__version__ = "1.0.0"

import json
import os
import socket
import threading
from datetime import datetime

import requests
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


# ============================================================
# 1. CONFIG  — REPLACE WITH YOUR FORM URL
# ============================================================
FORM_URL = "https://docs.google.com/forms/d/e/1mwo5IXXrIu4bnqR8GOV1qNxQ31rdfdUjeLfBQf22t1M/formResponse"

ENTRY_IDS = {
    "date_year":  "entry.2136503892_year",
    "date_month": "entry.2136503892_month",
    "date_day":   "entry.2136503892_day",
    "production": "entry.1158157721",
    "batch_no":   "entry.506973404",
    "batch_size": "entry.1883776086",
}

QUEUE_FILE = "production_queue.json"


# ============================================================
# 2. PRODUCTS (full 137)
# ============================================================
PRODUCTS = [
    "AFRABVITE 15ML DROPS",
    "AFRABVITE 100ML SYRUP",
    "ALLERGIN 60ML SYRUP",
    "AMIBAGYL 60ML SUSPENSION",
    "HOSPIMOX (AMOXYCILLIN) 125MG 100ML SUSPENSION",
    "CILLINOX SUSP. (AMPI/CLOX) 100MLS",
    "AMIBAGYL TABLETS 200MG",
    "BANEDIF OINTMENT",
    "BANEDIF POWDER",
    "CHEMOTRIM 100ML SUSPENSION",
    "CILLINOX 12ML DROPS",
    "CITRAMIN 15ML DROPS",
    "CHLORAF 100ML SUSPENSION",
    "CHEMOTRIM TAB 480MG (10X10)",
    "CHEMOTRIM 60ML SUSPENSION",
    "DETONIC 200ML SYRUP",
    "DIASTOP 100ML SUSPENSION",
    "DETONIC SYRUP (1 LTR)",
    "ENAPHRIN NASAL DROPS (10ML)",
    "FUNGUSOL 20GM CREAM",
    "FUNGUSOL 20GM POWDER",
    "FUNGUSOL 50ML LOTION",
    "GLIBENOL CAPLETS 5MG (10X10)",
    "AFRAB CHLOROQUINE DROPS 11ML",
    "AFRAB IBUPROFEN SUSPENSION",
    "LA-TESEN TABLETS",
    "NOSPAMIN 15ML DROPS",
    "NOCOF DROPS",
    "OTO MED 8ML DROPS",
    "PANDA 15ML DROPS",
    "PANDA 60ML SYRUP",
    "PANDA TABLET 96'S",
    "PANDA TABLET 1000'S",
    "PANDA COLD DROPS",
    "REUMEX LOTION",
    "STOPACID 200ML SUSPENSION",
    "TUSSYLIN 100ML SYRUP [Adult]",
    "TUSSYLIN 100ML SYRUP [Infant]",
    "CITRAMIN SYRUP 100ML",
    "CYSTAZOLE SUSPENSION",
    "HALOPERIDOL TABLETS (10MG)",
    "HALOPERIDOL TABLETS (5MG)",
    "PANDA COLD SYRUP",
    "PANDA NIGHT CAPLETS (500MG) 10X10",
    "CYSTAZOLE CAPLETS (200MG)",
    "NOCOF SYRUP",
    "FUNGUSOL PLUS CREAM",
    "FUNGUSOL PLUS LOTION",
    "AFRAB LORATADINE SYRUP (60ML)",
    "AFRAB LORATADINE TABS (10X10)",
    "AFRAB LORATADINE TABS 10MG (10 X 2)",
    "DETONIC PLUS SYRUP",
    "AFRAB METFORMIN TABLETS (3 X 10)",
    "PANDA NIGHT CAPLETS (12 X 8)",
    "AMIBAGYL TABLETS 200MG (1000'S)",
    "AFRABVITE PLUS DROPS",
    "AFRAMIN SYRUP (200ML)",
    "PANDA NIGHT SYRUP (60ML)",
    "AFRAB IVY SYRUP (100ML)",
    "THIVY SYRUP (100ML)",
    "AFRAB GRIPE WATER (100ML)",
    "STOPACID 200ML SUSPENSION (strawberry)",
    "STOPACID 200ML SUSPENSION (banana)",
    "PANDA SUSPENSION (60ML)",
    "AFRAB CIPROFLOXACIN CAPLET 500MG (10'S)",
    "PANDA NIGHT CAPLETS (2x10)",
    "PANDA CAPLETS 500mg (10X10)",
    "PANDA CAPLETS 500mg (10 X 2)",
    "PANDA NIGHT DROPS (15ML)",
    "AFRAGRA TABLETS (100MG (1 X 4)",
    "HOSPIMOX CAPSULES",
    "NOSPAMIN SYRUP",
    "AFRAB LEVOFLOXACIN CAPLET 500MG (10'S)",
    "CITRAMIN PLUS TAB (Effervescent)",
    "AFRAB ALENDOMAX 70mg",
    "B-Cor 2.5MG (10X3)",
    "B-Cor 5MG (15 X 2)",
    "B-Cor TABLETS 10MG (10 X 3)",
    "AFRAB RESPAL 1mg (2 X 10)",
    "AFRAB RISPERIDON 2mg (2 X 10)",
    "AFRAB RISPERIDON 4mg (2 X 10)",
    "PANDA EXTRA CAPLETS 500MG (10X10)",
    "AFRAB SALBUTAMOL SYRUP 100ML",
    "LATESEN DS CAPLETS (1 X 6)",
    "AFRAB SALBUTAMOL TABLET 4MG (10X10)",
    "ALFALEX CAPSULES 200MG (1 X 10)",
    "ALFALEX CAPSULES 400MG",
    "HISTOLAT SYRUP (60ML)",
    "HISTOLAT TABLETS (5MG)",
    "ALFADOX TABLETS (3x1)",
    "AFRAB IBUPROFEN DS DROPS 30ML",
    "ALFADOX SUSPENSION (15ML)",
    "AFRABRON SYRUP(200ML)",
    "ULTRA LINC TABLETS 5MG(2x15)",
    "ULTRA LINC TABLETS 20MG(1x4)",
    "AFRADIN DROPS(30ML)",
    "DEKOLIK SYRUP(60ML)",
    "AFRAB IBUPROFEN EFFERVESCENT",
    "AFRAB IBUPROFEN DS SUSPENSION 100ML",
    "PANDA EFFERVESCENT",
    "AFRAB TERAD DROPS(25ML)",
    "AFRAB SIMETHICONE DROPS",
    "TERAD CAPLETS (1X30)",
    "CITRAMIN DROPS 30ML",
    "AFRABVITE DROPS 30ML",
    "AFRABVITE PLUS DROPS 30ML",
    "PANDA DROPS 30ML",
    "NOCOF DROPS 30ML",
    "SOLOMAX SYRUP 100ML",
    "AFRABLEX SYRUP (100ML)",
    "AFRAB ZINC 11MG TABLETS(10 X 3)",
    "AFRAB LORATADINE SYRUP 100ML",
    "AFRAB ORS POWDER(3x1)",
    "AFRAB ZINC SULPHATE 20MG TABLETS(1 X 10)",
    "AFRAB HAND SANITIZER (100ML)",
    "METFORMIN TABLETS(10 X 10)",
    "AFRAB CHLOROQUINE TABLETS(1 x 10)",
    "LA-TESEN TABLETS 20/120MG (2 X 24)",
    "CETRAZEE TABLETS 60's",
    "AFRAB HYOSCINE BUTYLBROMIDE SYRUP",
    "LATESEN DISPERSIBLE TABS (6'S)",
    "DETONIC SYRUP (100ML)",
    "RESPERIDONE SYRUP",
    "IBUPROFEN TABLETS",
    "AFRABRON TABLETS(3 X 10)",
    "AFRAB LISINOPRIL TABLET 5MG(2 X 14)",
    "AFRAB LISINOPRIL TABLET 10MG(2 X 14)",
    "AFRAB AMLODIPINE TABLETS 5MG(2 X 14)",
    "AFRAB AMLODIPINE TABLETS 10MG(2 X 14)",
    "VITA JOY MOOD CARE TABLETS",
    "VITA JOY NEURO CARE TABLETS",
    "VITA JOY POSTNATAL CARE TABLETS",
    "VITA JOY PRENATAL CARE TABLETS",
    "VITA JOY SLEEP CARE TABLETS",
    "VITA JOY STRESS RELAX CARE TABLETS",
    "VITA JOY FEMALE TEEN CARE TABLETS",
    "VITA JOY MALE TEEN CARE TABLETS",
]


# ============================================================
# 3. HELPERS
# ============================================================
def get_app_dir():
    app = App.get_running_app()
    base = app.user_data_dir if app else os.path.expanduser("~")
    try:
        os.makedirs(base, exist_ok=True)
    except OSError:
        pass
    return base


def get_queue_path():
    return os.path.join(get_app_dir(), QUEUE_FILE)


def has_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3).close()
        return True
    except OSError:
        return False


def split_date(iso_date):
    if not iso_date:
        return "0", "0", "0"
    try:
        y, m, d = iso_date.split("-")
        return str(int(y)), str(int(m)), str(int(d))
    except ValueError:
        return "0", "0", "0"


def build_payload(data):
    y, m, d = split_date(data.get("date", ""))
    return {
        ENTRY_IDS["date_year"]:  y,
        ENTRY_IDS["date_month"]: m,
        ENTRY_IDS["date_day"]:   d,
        ENTRY_IDS["production"]: data.get("production", ""),
        ENTRY_IDS["batch_no"]:   data.get("batch_no", ""),
        ENTRY_IDS["batch_size"]: data.get("batch_size", ""),
    }


def try_submit(data):
    try:
        r = requests.post(FORM_URL, data=build_payload(data), timeout=15)
        if r.status_code not in (200, 201, 202):
            return False
        if "accounts.google.com" in r.url:
            return False
        return True
    except requests.RequestException:
        return False


def load_queue():
    path = get_queue_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_queue(queue):
    try:
        with open(get_queue_path(), "w", encoding="utf-8") as f:
            json.dump(queue, f)
    except OSError:
        pass


def save_to_queue(data):
    q = load_queue()
    q.append(data)
    save_queue(q)


def flush_queue():
    q = load_queue()
    if not q:
        return 0
    remaining, sent = [], 0
    for item in q:
        if try_submit(item):
            sent += 1
        else:
            remaining.append(item)
    save_queue(remaining)
    return sent


# ============================================================
# 4. SEARCHABLE PICKER (with custom entry)
# ============================================================
class ProductPicker(Popup):
    def __init__(self, on_pick, **kwargs):
        super().__init__(title="Select Production", size_hint=(0.95, 0.9), **kwargs)
        self.on_pick = on_pick

        root = BoxLayout(orientation="vertical", padding=8, spacing=8)

        custom_row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(6))
        self.custom_input = TextInput(hint_text="Or type custom product...",
                                      multiline=False, font_size=dp(14))
        custom_row.add_widget(self.custom_input)
        custom_btn = Button(text="Use", size_hint_x=0.25, font_size=dp(14),
                            background_color=(0.15, 0.55, 0.85, 1))
        custom_btn.bind(on_release=self.use_custom)
        custom_row.add_widget(custom_btn)
        root.add_widget(custom_row)

        self.search = TextInput(hint_text="Search list...", multiline=False,
                                size_hint_y=None, height=dp(44), font_size=dp(14))
        self.search.bind(text=self.refresh)
        root.add_widget(self.search)

        self.scroll = ScrollView()
        self.list_layout = BoxLayout(orientation="vertical",
                                     size_hint_y=None, spacing=2)
        self.list_layout.bind(minimum_height=self.list_layout.setter("height"))
        self.scroll.add_widget(self.list_layout)
        root.add_widget(self.scroll)

        self.add_widget(root)
        self.refresh(None, "")

    def use_custom(self, instance):
        text = self.custom_input.text.strip()
        if text:
            self.on_pick(text)
            self.dismiss()

    def refresh(self, instance, value):
        self.list_layout.clear_widgets()
        q = (value or "").strip().lower()
        items = [p for p in PRODUCTS if q in p.lower()] if q else PRODUCTS
        for item in items:
            btn = Button(text=item, size_hint_y=None, height=dp(44),
                         halign="left", valign="middle", font_size=dp(14))
            btn.bind(on_release=lambda b, t=item: self.pick(t))
            self.list_layout.add_widget(btn)

    def pick(self, text):
        self.on_pick(text)
        self.dismiss()


# ============================================================
# 5. PREVIEW POPUP
# ============================================================
class PreviewPopup(Popup):
    def __init__(self, data, on_confirm, **kwargs):
        super().__init__(title="Review Before Sending",
                         size_hint=(0.9, 0.7), **kwargs)
        self.on_confirm = on_confirm

        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))

        preview_text = (
            f"[b]Date:[/b] {data['date']}\n\n"
            f"[b]Production:[/b] {data['production']}\n\n"
            f"[b]Batch No:[/b] {data['batch_no']}\n\n"
            f"[b]Batch Size:[/b] {data['batch_size']} bottles"
        )
        root.add_widget(Label(text=preview_text, markup=True,
                              font_size=dp(15), halign="left",
                              valign="top"))

        btns = BoxLayout(size_hint_y=None, height=dp(56), spacing=dp(10))
        confirm_btn = Button(text="Confirm & Send", font_size=dp(15), bold=True,
                             background_color=(0.2, 0.7, 0.3, 1))
        confirm_btn.bind(on_release=lambda *a: self.confirm())
        btns.add_widget(confirm_btn)
        edit_btn = Button(text="Go Back", font_size=dp(15),
                          background_color=(0.5, 0.5, 0.5, 1))
        edit_btn.bind(on_release=lambda *a: self.dismiss())
        btns.add_widget(edit_btn)
        root.add_widget(btns)

        self.add_widget(root)

    def confirm(self):
        self.on_confirm()
        self.dismiss()


# ============================================================
# 6. MAIN UI
# ============================================================
class ProductionBatchTrackerForm(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        Window.softinput_mode = "below_target"

        self.selected_production = ""

        # Header
        self.add_widget(Label(
            text="Production Batch Tracker",
            font_size=dp(20), bold=True, size_hint_y=None,
            height=dp(48), color=(0.15, 0.45, 0.85, 1),
        ))

        # Scrollable form
        scroll = ScrollView(size_hint=(1, 1))
        form = BoxLayout(orientation="vertical", spacing=dp(10),
                         padding=dp(12), size_hint_y=None)
        form.bind(minimum_height=form.setter("height"))

        # Date
        form.add_widget(Label(text="Date:", size_hint_y=None, height=dp(24),
                              halign="left", font_size=dp(14)))
        self.date_input = TextInput(text=datetime.now().strftime("%Y-%m-%d"),
                                    multiline=False, size_hint_y=None,
                                    height=dp(50), font_size=dp(15))
        form.add_widget(self.date_input)

        # Production
        form.add_widget(Label(text="Production Name:", size_hint_y=None,
                              height=dp(24), halign="left", font_size=dp(14)))
        self.prod_btn = Button(text="Tap to choose production",
                               size_hint_y=None, height=dp(52), font_size=dp(15),
                               background_color=(0.2, 0.6, 0.85, 1))
        self.prod_btn.bind(on_release=self.open_picker)
        form.add_widget(self.prod_btn)

        # Batch No
        form.add_widget(Label(text="Batch No:", size_hint_y=None, height=dp(24),
                              halign="left", font_size=dp(14)))
        self.batch_input = TextInput(hint_text="e.g. B-101", multiline=False,
                                     size_hint_y=None, height=dp(50),
                                     font_size=dp(15))
        form.add_widget(self.batch_input)

        # Batch Size
        form.add_widget(Label(text="Batch Size (bottles):", size_hint_y=None,
                              height=dp(24), halign="left", font_size=dp(14)))
        self.size_input = TextInput(hint_text="e.g. 5000", multiline=False,
                                    input_type="number", size_hint_y=None,
                                    height=dp(50), font_size=dp(15))
        form.add_widget(self.size_input)

        scroll.add_widget(form)
        self.add_widget(scroll)

        # Status
        self.status = Label(text="Ready",
                            size_hint_y=None, height=dp(30),
                            font_size=dp(13), color=(0.3, 0.5, 0.3, 1))
        self.add_widget(self.status)

        # Buttons
        btn_row = BoxLayout(size_hint_y=None, height=dp(64),
                            spacing=dp(6), padding=dp(6))

        preview_btn = Button(text="Preview & Send", font_size=dp(15), bold=True,
                             background_color=(0.2, 0.7, 0.3, 1))
        preview_btn.bind(on_release=self.preview)
        btn_row.add_widget(preview_btn)

        sync_btn = Button(text="Sync", font_size=dp(15), bold=True,
                          background_color=(0.9, 0.6, 0.2, 1))
        sync_btn.bind(on_release=self.sync_queue)
        btn_row.add_widget(sync_btn)

        clear_btn = Button(text="Clear", font_size=dp(15), bold=True,
                           background_color=(0.8, 0.3, 0.3, 1))
        clear_btn.bind(on_release=self.clear_form)
        btn_row.add_widget(clear_btn)

        self.add_widget(btn_row)

        # Auto-sync
        Clock.schedule_once(lambda dt: self._background_sync(0), 3)
        Clock.schedule_interval(self._background_sync, 30)

    def open_picker(self, instance):
        ProductPicker(on_pick=self.set_production).open()

    def set_production(self, name):
        self.selected_production = name
        self.prod_btn.text = name

    def collect(self):
        return {
            "date":       self.date_input.text.strip(),
            "production": self.selected_production,
            "batch_no":   self.batch_input.text.strip(),
            "batch_size": self.size_input.text.strip(),
        }

    def preview(self, instance):
        data = self.collect()
        if not data["production"]:
            self.status.text = "Choose a production first."
            self.status.color = (0.9, 0.1, 0.1, 1)
            return
        if not all(data.values()):
            self.status.text = "Fill in every field."
            self.status.color = (0.9, 0.1, 0.1, 1)
            return
        PreviewPopup(data=data, on_confirm=lambda: self.send_now(data)).open()

    def send_now(self, data):
        if try_submit(data):
            self.status.text = "Submission successful."
            self.status.color = (0.3, 0.5, 0.3, 1)
            self.clear_form()
        else:
            save_to_queue(data)
            if has_internet():
                self.status.text = "Saved locally — will retry shortly."
            else:
                self.status.text = "Saved offline. Will auto-sync."
            self.status.color = (0.9, 0.55, 0.1, 1)
            Clock.schedule_once(lambda dt: self._background_sync(0), 5)

    def _background_sync(self, dt):
        if not load_queue():
            return
        if not has_internet():
            return
        threading.Thread(target=self._do_sync, daemon=True).start()

    def _do_sync(self):
        sent = flush_queue()
        if sent > 0:
            Clock.schedule_once(lambda dt: self._on_sync_done(sent), 0)

    def _on_sync_done(self, count):
        self.status.text = f"Auto-synced {count} item(s)."
        self.status.color = (0.3, 0.5, 0.3, 1)

    def sync_queue(self, instance):
        sent = flush_queue()
        self.status.text = f"Synced {sent} item(s)." if sent else "Nothing to sync."
        self.status.color = (0.3, 0.5, 0.3, 1)

    def clear_form(self, instance=None):
        self.selected_production = ""
        self.prod_btn.text = "Tap to choose production"
        self.batch_input.text = ""
        self.size_input.text = ""
        self.date_input.text = datetime.now().strftime("%Y-%m-%d")


# ============================================================
# 7. APP
# ============================================================
class ProductionBatchTrackerApp(App):
    def build(self):
        self.title = "Production Batch Tracker"
        return ProductionBatchTrackerForm()


if __name__ == "__main__":
    ProductionBatchTrackerApp().run()

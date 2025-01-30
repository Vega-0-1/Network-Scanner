class Localization:
    def __init__(self):
        self.language = "en"
        self.translations = {
            "en": {
                "start_scan": "Start Scan",
                "advanced_scan": "Advanced Scan",
                "exit": "Exit",
                "network_interface": "Network Interface",
                "port_range": "Port Range",
                "default": "Default (1-1024)",
                "full_range": "Full Range (1-65535)",
                "custom_range": "Custom Range",
                "to": "to",
                "ip_scan_progress": "IP Scan Progress",
                "port_scan_progress": "Port Scan Progress",
                "scan_complete": "Scan Complete",
                "advanced_scan_complete": "Advanced Scan Complete",
                "error_select_interface": "Please select a network interface.",
                "Settings": "Settings",
                "Theme": "Theme",
                "Language": "Language",
                "Active": "Active",
                "Inactive": "Inactive",
                "close": "Close",
                "Progress": "Progress",
                "Error": "Error"
            },
            "he": {
                "start_scan": "התחל סריקה",
                "advanced_scan": "סריקה מתקדמת",
                "exit": "יציאה",
                "network_interface": "ממשק רשת",
                "port_range": "טווח פורטים",
                "default": "ברירת מחדל (1-1024)",
                "full_range": "טווח מלא (1-65535)",
                "custom_range": "טווח מותאם אישית",
                "to": "עד",
                "ip_scan_progress": "התקדמות סריקת IP",
                "port_scan_progress": "התקדמות סריקת פורטים",
                "scan_complete": "הסריקה הושלמה",
                "advanced_scan_complete": "סריקה מתקדמת הושלמה",
                "error_select_interface": "אנא בחר ממשק רשת.",
                "Settings": "הגדרות",
                "Theme": "נושא",
                "Language": "שפה",
                "Active": "פעיל",
                "Inactive": "לא פעיל",
                "close": "סגור",
                "Progress": "התקדמות",
                "Error": "שגיאה"
            }
        }

    def set_language(self, language):
        """Set the current language."""
        if language in self.translations:
            self.language = language
        else:
            raise ValueError("Unsupported language")

    def translate(self, key):
        """Translate a key based on the current language."""
        return self.translations.get(self.language, {}).get(key, key)

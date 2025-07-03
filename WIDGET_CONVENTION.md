# Widget Naming Guideline

This document provides naming conventions and abbreviations for commonly used UI widgets to ensure consistency and
clarity in your codebase.

---

## 🔹 General Naming Rules

- Use `snake_case` for variable and attribute names.
- Prefix private widget variables with `__` (double underscore).
- Use short but clear abbreviations for widget types.
- Keep the purpose or content of the widget in the name.

---

## 🔸 Common Widget Abbreviations

| Widget Type     | Suggested Abbreviation | Example                  |
|-----------------|------------------------|--------------------------|
| Button          | `btn`                  | `__btn_submit`           |
| Checkbox        | `chk`                  | `__chk_agree_terms`      |
| Toggle          | `tgl`                  | `__tgl_dark_mode`        |
| Panel/Container | `pnl`                  | `__pnl_trade_info`       |
| Sidebar         | `sb`                   | `__sb_navigation`        |
| Section         | `sec`                  | `__sec_profile_settings` |
| Switch          | `swt`                  | `__swt_notifications`    |
| Dropdown        | `ddl` / `dd`           | `__ddl_country_select`   |
| Tab             | `tab`                  | `__tab_overview`         |
| Input Field     | `inp`                  | `__inp_email`            |
| Label/Text      | `lbl` / `txt`          | `__lbl_user_name`        |
| Icon            | `ico`                  | `__ico_close`            |
| Dialog/Modal    | `dlg`                  | `__dlg_confirm_delete`   |
| Table/Grid      | `tbl` / `grid`         | `__tbl_trade_history`    |
| Tooltip         | `tip`                  | `__tip_balance_info`     |
| Form            | `frm`                  | `__frm_registration`     |

---

## 🔸 Examples

```python
__btn_submit        # Submit button
__chk_agree_terms   # Terms & Conditions checkbox
__tgl_one_click     # One-click trading toggle
__pnl_trade_detail  # Panel for showing trade details
__sb_settings       # Sidebar for settings
__inp_quantity      # Input field for quantity

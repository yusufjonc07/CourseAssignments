"""Simple Tkinter GUI to load CSV, preview, run pipeline and export results."""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from typing import Optional
from .pipeline import pipeline_clean_and_aggregate
from .forecast import train_and_forecast
from .visualize import plot_category_bar, plot_forecast_series


class DDPApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title('DDP: Data Processing & Forecast')
        root.geometry('900x600')

        # brief description
        desc = ('Load a transactions CSV, preview rows, run cleaning/aggregation, '
                'and produce a 1-month forecast with visualizations.')
        ttk.Label(root, text='DDP — Data Processing & Forecast', font=('Segoe UI', 16, 'bold')).pack(pady=(10, 0))
        ttk.Label(root, text=desc, wraplength=800).pack(pady=(0, 10))

        frm = ttk.Frame(root)
        frm.pack(fill='x', padx=12)

        ttk.Button(frm, text='Open CSV', command=self.open_csv).pack(side='left')
        ttk.Button(frm, text='Run Pipeline', command=self.run_pipeline).pack(side='left', padx=8)
        ttk.Button(frm, text='Run Forecast', command=self.run_forecast).pack(side='left', padx=8)
        ttk.Button(frm, text='Save Aggregated CSV', command=self.save_agg).pack(side='left', padx=8)

        # treeview for preview
        self.tree = ttk.Treeview(root)
        self.tree.pack(fill='both', expand=True, padx=12, pady=12)

        self.df: Optional[pd.DataFrame] = None
        self.aggregated: Optional[pd.DataFrame] = None

    def open_csv(self):
        path = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv'), ('All files', '*.*')])
        if not path:
            return
        try:
            df = pd.read_csv(path)
        except Exception as e:
            messagebox.showerror('Error', f'Failed to read CSV: {e}')
            return
        self.df = df
        self._show_dataframe_preview(df)

    def _show_dataframe_preview(self, df: pd.DataFrame, max_rows: int = 200):
        # clear
        for c in self.tree.get_children():
            self.tree.delete(c)
        self.tree['columns'] = list(df.columns[:20])
        self.tree['show'] = 'headings'
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor='w')
        preview = df.head(max_rows).fillna('')
        for _, row in preview.iterrows():
            vals = [str(row[c]) for c in self.tree['columns']]
            self.tree.insert('', 'end', values=vals)

    def run_pipeline(self):
        if self.df is None:
            messagebox.showwarning('No data', 'Open a CSV first.')
            return
        try:
            self.aggregated = pipeline_clean_and_aggregate(self.df)
        except Exception as e:
            messagebox.showerror('Error', f'Pipeline failed: {e}')
            return
        messagebox.showinfo('Done', 'Aggregation complete — previewing result')
        self._show_dataframe_preview(self.aggregated)

    def run_forecast(self):
        if self.aggregated is None:
            messagebox.showwarning('No aggregated data', 'Run pipeline first.')
            return
        try:
            monthly_pivot = self.aggregated.pivot(index='month', columns='category_clean', values='amount_imputed').fillna(0)
            monthly_pivot['total_all'] = monthly_pivot.sum(axis=1)
            pred_mean, pred_ci, forecast_series = train_and_forecast(monthly_pivot)
        except Exception as e:
            messagebox.showerror('Error', f'Forecast failed: {e}')
            return
        # show visualizations
        latest_month = monthly_pivot.index.max()
        latest_totals = monthly_pivot.loc[latest_month].drop('total_all')
        plot_category_bar(latest_totals, latest_month)
        plot_forecast_series(forecast_series, actual_series_index=forecast_series.index[:-1], pred_mean=pred_mean, pred_ci=pred_ci) # type: ignore
        messagebox.showinfo('Forecast', f'Predicted total: {pred_mean:.2f}\n95% CI: [{pred_ci[0]:.2f}, {pred_ci[1]:.2f}]')

    def save_agg(self):
        if self.aggregated is None:
            messagebox.showwarning('No aggregated data', 'Run pipeline first.')
            return
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')])
        if not path:
            return
        try:
            self.aggregated.to_csv(path, index=False)
        except Exception as e:
            messagebox.showerror('Error', f'Failed to save CSV: {e}')
            return
        messagebox.showinfo('Saved', f'Aggregated CSV saved to {path}')


def run_gui():
    root = tk.Tk()
    app = DDPApp(root)
    root.mainloop()

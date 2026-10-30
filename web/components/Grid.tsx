"use client";

import { AllCommunityModule, ModuleRegistry, colorSchemeDark, themeQuartz, type ColDef } from "ag-grid-community";
import { AgGridReact } from "ag-grid-react";
import { useEffect, useState } from "react";

ModuleRegistry.registerModules([AllCommunityModule]);

const light = themeQuartz.withParams({ fontSize: 13, headerFontWeight: 600 });
const dark = light.withPart(colorSchemeDark);

export function Grid<T>({ rows, cols, height = 320, onRowClicked }: {
  rows: T[];
  cols: ColDef<T>[];
  height?: number;
  onRowClicked?: (row: T) => void;
}) {
  const [isDark, setDark] = useState(false);
  useEffect(() => {
    const m = window.matchMedia("(prefers-color-scheme: dark)");
    setDark(m.matches);
    const on = (e: MediaQueryListEvent) => setDark(e.matches);
    m.addEventListener("change", on);
    return () => m.removeEventListener("change", on);
  }, []);
  return (
    <div className="grid-host" style={{ height }}>
      <AgGridReact<T>
        theme={isDark ? dark : light}
        rowData={rows}
        columnDefs={cols}
        defaultColDef={{ sortable: true, resizable: true, flex: 1, minWidth: 90 }}
        onRowClicked={onRowClicked ? (e) => e.data && onRowClicked(e.data) : undefined}
        rowSelection={onRowClicked ? { mode: "singleRow", checkboxes: false, enableClickSelection: true } : undefined}
      />
    </div>
  );
}

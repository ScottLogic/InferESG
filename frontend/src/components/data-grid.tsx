/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { useMemo } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import { ColDef } from 'ag-grid-community';
import styles from './data-grid.module.css';

const dateFormatter = (params: any) => {
  const date = new Date(params.value);
  // Format date to 'dd MMM yyyy'
  return date.toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  });
};

const numberFormatter = (params: any) => {
  const value = parseFloat(params.value);
  if (isNaN(value)) {
    return;
  }

  return Number.isSafeInteger(value)
    ? parseInt(params.value)
    : value.toFixed(2);
};

const booleanFormatter = (params: any) => {
  if (
    params.value === true ||
    params.value.toString().toLowerCase() === 'true'
  ) {
    return true;
  }

  return false;
};

const determineCellDataType = (value: any) => {
  if (typeof value === 'object') {
    return 'object';
  }

  // regex numeric only
  if (!isNaN(value) && /^[+-]?(\d+)$/.test(value)) {
    return 'number';
  }

  // regex for numeric with decimal 00000.00
  if (!isNaN(value) && /^[+-]?(\d*\.\d+)$/.test(value)) {
    return 'float';
  }

  // not only numbers (regex) && can be parsed as a date
  if (!/^\d+$/.test(value) && !isNaN(Date.parse(value))) {
    return 'date';
  }

  if (
    value === true ||
    value === false ||
    value.toLowerCase() === 'true' ||
    value.toLowerCase() === 'false'
  ) {
    return 'boolean';
  }

  return 'string';
};

const createGetterForKey = (prefix: string[], key: string) => {
  return (obj: any) => {
    let o = obj?.data;
    for (const p of prefix) {
      o = o?.[p];
    }
    return o?.[key];
  };
};

const columnMapStrategy = (
  key: any,
  value: any,
  prefix: string[] = [],
): any => {
  let columnTypeProps = {};
  switch (determineCellDataType(value)) {
    case 'object':
      // flattern nested objects
      return Object.entries(value).flatMap(([innerKey, innerValue]) =>
        columnMapStrategy(innerKey, innerValue, [...prefix, key]),
      );
    case 'date':
      columnTypeProps = {
        ...columnTypeProps,
        cellDataType: 'date',
        valueFormatter: dateFormatter,
      };
      break;
    case 'number':
      columnTypeProps = {
        ...columnTypeProps,
        cellDataType: 'number',
        valueFormatter: numberFormatter,
      };
      break;
    case 'boolean':
      columnTypeProps = {
        ...columnTypeProps,
        cellDataType: 'boolean',
        valueFormatter: booleanFormatter,
      };
      break;
    default:
      break;
  }

  const headerName = key.replace(/^[a-z]\./, '');

  return {
    field: prefix?.length ? undefined : key,
    valueGetter: prefix?.length ? createGetterForKey(prefix, key) : undefined,
    headerName,
    ...columnTypeProps,
  };
};

const getColumnDefs = (dataset: any) => {
  if (
    dataset === undefined ||
    dataset.length === 0 ||
    !Array.isArray(dataset)
  ) {
    return [];
  }

  return Object.entries(dataset[0]).flatMap(([key, value]) =>
    columnMapStrategy(key, value),
  );
};

export interface DataGridProps {
  dataset: any[] | undefined;
}

export const DataGrid = ({ dataset }: DataGridProps) => {
  const defaultColDef = useMemo<ColDef>(() => {
    return {
      flex: 1,
      minWidth: 100,
      sortable: true,
      resizable: true,
      filter: true,
      floatingFilter: true,
    };
  }, [dataset]);

  const colDefs = useMemo(() => getColumnDefs(dataset), [dataset]);

  return (
    <div className={styles.container}>
      <div
        className={'ag-theme-quartz'}
        style={{ width: '100%', height: '100%' }}
      >
        {dataset && (
          <AgGridReact
            rowData={dataset}
            columnDefs={colDefs}
            defaultColDef={defaultColDef}
            paginationAutoPageSize={true}
            pagination={true}
            suppressFieldDotNotation={true}
          />
        )}
      </div>
    </div>
  );
};

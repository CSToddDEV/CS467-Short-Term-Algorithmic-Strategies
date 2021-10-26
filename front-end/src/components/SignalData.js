import React from 'react';

const mockHeaders = ['Ticker', 'Date-time', 'Sign', 'Price'];

const mockData = [
  ['TQQQ', '10/8/21 14:43:52', 'BUY', '130.67'],
  ['UPRO', '10/6/21 10:12:23', 'SELL', '136.31'],
  ['TQQQ', '10/5/21 15:08:29', 'SELL', '138.05'],
  ['FAS', '10/5/21 11:57:13', 'BUY', '126.93']
];

function SignalData() {
    return (
      <div className="data content">
        <h1>Signal Data</h1>
        <DataTable 
          headers={mockHeaders}
          dataRows={mockData}
        />
      </div>
    );
}

class DataTable extends React.Component {
  generateHeaders() {
    let table_headers = [];
    this.props.headers.forEach(header => {
      table_headers.push(<th>{header}</th>)
    });

    return table_headers;
  }

  generateRows() {
    let table_rows = [];

    this.props.dataRows.forEach(dataRow => {
      let newRow = [];
      dataRow.forEach(item => {
        newRow.push(<td>{item}</td>);
      });
      table_rows.push(<tr>{newRow}</tr>);
    });

    return table_rows;
  }

  render() {
    let table_headers = this.generateHeaders();
    let table_rows = this.generateRows();

    return (
      <table>
        <thead><tr>{table_headers}</tr></thead>
        <tbody>{table_rows}</tbody>
      </table>
    );
  }
}
  
export default SignalData;
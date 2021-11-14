import React from 'react';
import {authFetch} from "./App";

const dataHeaders = ['Tracked Ticker', 'Date', 'Signal', '% invested'];

function SignalData() {
    return (
      <div className="data content">
        <h1>Signal Data</h1>
        <DataTable 
          headers={dataHeaders}
        />
      </div>
    );
}

class DataTable extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        signals: [],
        isLoading: true
      }
  }

  componentDidMount() {
      authFetch('/3stat/signals/', {
          method: 'get',
          headers: {
              'Content-Type': 'application/json'
          }
        }).then( res => res.json()
        ).then( data => {
            this.setState({
            signals: data,
            isLoading: false
            })
      }).catch( (error) => {
        console.log(error);
      });
  }

  generateHeaders() {
    let table_headers = [];
    this.props.headers.forEach(header => {
      table_headers.push(<th>{header}</th>)
    });

    return table_headers;
  }

  generateRows() {
    let table_rows = [];

    console.log("ROWS", this.state.signals.result);
    this.state.signals.result.forEach(signalData => {
      let newRow = [];
      newRow.push(<td>{signalData.ticker}</td>);
      newRow.push(<td>{signalData.date}</td>);
      newRow.push(<td>{signalData.signal}</td>);
      newRow.push(<td>{signalData.total_invested + "%"}</td>);

      table_rows.push(<tr key={signalData.id}>{newRow}</tr>);
    });

    return table_rows;
  }

  render() {
    if (this.state.isLoading) {
      return (
        <p>Data is loading...</p>
      );
    } else {
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
}
  
export default SignalData;
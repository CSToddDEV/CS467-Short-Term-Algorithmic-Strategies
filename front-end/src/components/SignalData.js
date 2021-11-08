import React from 'react';
import axios from 'axios';

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
    axios.get('https://www.cstodd.dev/3stat/signals/')
      .then( (response) => {
        console.log("response", response);
        console.log("data", response.data);
        this.setState({
          signals: response.data.result,
          isLoading: false
        });
      })
      .catch( (error) => {
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

    this.state.signals.forEach(signalData => {
      let newRow = [];
      newRow.push(<td>{signalData.ticker}</td>);
      newRow.push(<td>{signalData.date}</td>);
      newRow.push(<td>{signalData.signal}</td>);
      newRow.push(<td>{signalData.total_invested + "%"}</td>);
      
      table_rows.push(<tr>{newRow}</tr>);
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
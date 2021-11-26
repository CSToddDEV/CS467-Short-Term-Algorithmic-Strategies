import React from 'react';
import { PieChart } from 'react-minimal-pie-chart';
import {authFetch} from "./App";

const defaultLabelStyle = {
    fontSize: '5px',
    fontFamily: 'sans-serif',
};

const colors = [
    '#86e39f',
    '#11782c',
    '#65d900',
    '#789163'
];

class Portfolio extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        ticker: "",
        percent_invested: 0,
        isLoading: true,
        dataAvailable: true,
        serverError: false
      }
  }

  componentDidMount() {
    authFetch('/3stat/signals/', {
          method: 'get',
          headers: {
              'Content-Type': 'application/json'
          }
        }).then( response => response.json()
         ).then( data => {
            if (data.result.length === 0) {
              this.setState({
                dataAvailable: false,
                isLoading: false
              });
            } else {
              console.log(data.result.at(-1).ticker);
              this.setState({
                  ticker: data.result.at(-1).ticker,
                  percent_invested: data.result.at(-1).total_invested,
                  isLoading: false
              });
            }
      })
      .catch( (error) => {
        console.log(error);
        this.setState({
          serverError: true,
          isLoading: false
        });
      }); 
  }

  makeGraphData() {
      let dataValues = [];
      let colorIndex = 0;
      let cashPercent = 100 - this.state.percent_invested;
      if (cashPercent > 0) {
        dataValues.push({title: 'CASH', value: cashPercent, color: colors[colorIndex]});
        colorIndex++;
      }
      if (this.state.percent_invested > 0) {
        dataValues.push({title: this.state.ticker, value: this.state.percent_invested, color: colors[colorIndex]});
      }

      return dataValues;
  }
  
  render() {
    if (this.state.isLoading) {
      return (<h3>Data loading...</h3>);
    } 
    else if (!(this.state.dataAvailable)) {
      return (<h3>No data currently available</h3>);
    }
    else if (this.state.serverError) {
      return (<h3>Server error - could not retrieve the requested data</h3>);
    }
    else {
      return (
        <div className="portfolio content">
          <h1>Current Portfolio Holdings</h1>
          <PieChart
              data={this.makeGraphData()}
              label={({ x, y, dx, dy, dataEntry }) => (
                  <text
                    x={x}
                    y={y}
                    dx={dx}
                    dy={dy}
                    dominant-baseline="central"
                    text-anchor="middle"
                    style={{
                      fontSize: '5px',
                      fontFamily: 'sans-serif',
                    }}
                  >
                    {Math.round(dataEntry.percentage) + '% ' + dataEntry.title}
                  </text>
              )}
              labelStyle={defaultLabelStyle}
              labelPosition={60}
              segmentsShift={0.4}
              radius={45}
          />
        </div>
      );
    }
  }
}

export default Portfolio;
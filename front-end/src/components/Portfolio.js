import React from 'react';
import { PieChart } from 'react-minimal-pie-chart';
import axios from 'axios';

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
        isLoading: true
      }
  }

  componentDidMount() {
    axios.get('https://www.cstodd.dev/3stat/signals/')
      .then( (response) => {
        console.log("response", response);
        console.log("data", response.data);
        let signals = response.data.result;
        let lastSignal = signals[signals.length - 1];
        console.log(lastSignal);
        this.setState({
          ticker: lastSignal.ticker,
          percent_invested: lastSignal.total_invested,
          isLoading: false
        });
      })
      .catch( (error) => {
        console.log(error);
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
      return (<p>Data loading...</p>);
    } else {
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
                    {Math.round(dataEntry.percentage) + '%' + ' ' + dataEntry.title}
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
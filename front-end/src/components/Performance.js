import React from 'react';
import axios from 'axios';

const periods = ['2 weeks', '1 month', '6 months', '1 year'];

const metricsMap = new Map();
metricsMap.set('2 weeks', {
    period: '2 weeks',
    rate_of_return: 3,
    benchmark_ror: 1,
    drawdown: -2
});
metricsMap.set('1 month', {
    period: '1 month',
    rate_of_return: 5,
    benchmark_ror: 3,
    drawdown: -3
});
metricsMap.set('6 months', {
    period: '6 months',
    rate_of_return: 10,
    benchmark_ror: 4,
    drawdown: -5
});
metricsMap.set('1 year', {
    period: '1 year',
    rate_of_return: 30,
    benchmark_ror: 7,
    drawdown: -9
});

function Performance() {
    return (
      <div className="performance content">
        <h1>Performance Metrics</h1>
        <MetricsView />
      </div>
    );
}

class MetricsView extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        currentPeriod: '2 weeks',
        startingCash: 1000,
        tempCash: 1000,
        isLoading: true
    }
    this.onClick = this.handleClick.bind(this);
    this.onSubmit = this.handleSubmit.bind(this);
    this.onChange = this.handleChange.bind(this);
  }

  handleClick(event) {
    this.setState({currentPeriod: event.target.name});
  }

  handleSubmit(event) {
      event.preventDefault();

      let newValue = parseFloat(this.state.tempCash);

      if (!Number.isNaN(newValue)) {
        this.setState({startingCash: newValue});
      }
  }

  handleChange(event) {
      this.setState({tempCash: event.target.value});
  }

  generatePeriodHeaders() {
    let headers = [];

    periods.forEach(period => {
        if (period === this.state.currentPeriod) {
            headers.push(<button className="selectedBtn" name={period} onClick={this.onClick}>{period}</button>);
        } else {
            headers.push(<button name={period} onClick={this.onClick}>{period}</button>);
        }
        
    });

    return headers;
  }

  setTwoDecimals(initialValue) {
    return (Math.round(initialValue * 100) / 100).toFixed(2);
  }

  buildMetricRow(metricName, percentValue) {
    let signChar = '+';
    if (percentValue < 0) {
        signChar = '-';
        percentValue *= -1;
    }

    return (
    <tr>
        <td>{metricName}</td>
        <td>{signChar + percentValue.toString() + '%'}</td>
        <td>{signChar + '$' + (this.setTwoDecimals((percentValue / 100) * this.state.startingCash)).toString()}</td>
    </tr>
    );
  }

  generateMetricRows() {
      let metricRows = [];
      let currentMetrics = metricsMap.get(this.state.currentPeriod);

      metricRows.push(this.buildMetricRow('Rate of return', currentMetrics.rate_of_return));
      metricRows.push(this.buildMetricRow('S&P 500 rate of return', currentMetrics.benchmark_ror));
      metricRows.push(this.buildMetricRow('Maximum drawdown', currentMetrics.drawdown));

      return metricRows;
  }

  render() {
    let periodHeaders = this.generatePeriodHeaders();
    let metricRows = this.generateMetricRows();

    return (
        <div className="metricsView">
            <form onSubmit={this.onSubmit}>
                <label for="startingCash" className="performanceLabel">Starting cash ($):</label> 
                <input name="startingCash" type="text" value={this.state.tempCash} onChange={this.onChange} />
                <input type="submit" value="Set" />
            </form>
            <br></br>
            <div className="periodTabs">
                <span className="performanceLabel">Time Period: </span>
                {periodHeaders}
            </div>
            <table className="metricsTable">
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>% change</th>
                        <th>Dollar change <br></br>(based on starting cash)</th>
                    </tr>
                </thead>
                <tbody>{metricRows}</tbody>
            </table>
        </div>
    );
  }
}
  
export default Performance;
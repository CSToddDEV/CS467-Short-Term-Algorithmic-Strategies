import React from 'react';

const periods = ['2 Weeks', '1 Month', '3 Months', '6 Months', '1 Year'];

const metricsMap = new Map();

let today = new Date();
const mockDate = today.toDateString();

function Performance(metricsMap) {
    return (
      <div className="performance content">
        <h1>Performance Metrics</h1>
        <MetricsView map={metricsMap} />
      </div>
    );
}

class MetricsView extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        currentPeriod: '2 Weeks',
        startingCash: 1000,
        tempCash: 1000,
        isLoading: true,
        dataAvailable: true,
        serverError: false
    }
    this.onClick = this.handleClick.bind(this);
    this.onSubmit = this.handleSubmit.bind(this);
    this.onChange = this.handleChange.bind(this);
  }

  componentDidMount() {
    fetch('/3stat/stats/', {
          method: 'get',
          headers: {
              'Content-Type': 'application/json'
          }
        }).then( response => response.json()
         ).then( data => {
            console.log(data.result);
            if (data.result.length === 0) {
                console.log("no data");
                this.setState({
                    dataAvailable: false,
                    isLoading: false
                });
            } else {
                this.setState({
                    stats: data.result
                });
            }
      }).then( () => {
        if (this.state.dataAvailable) {
            metricsMap.set('2 Weeks', {
                period: '2 Weeks',
                rate_of_return: this.state.stats.at(4).rate_of_return,
                benchmark_ror: this.state.stats.at(4).benchmark_ror[0][0].ror,
                drawdown: this.state.stats.at(4).drawdown
            });
            metricsMap.set('1 Month', {
                period: '1 Month',
                rate_of_return: this.state.stats.at(3).rate_of_return,
                benchmark_ror: this.state.stats.at(3).benchmark_ror[0][0].ror,
                drawdown: this.state.stats.at(3).drawdown
            });
            metricsMap.set('3 Months', {
                period: '3 Months',
                rate_of_return: this.state.stats.at(2).rate_of_return,
                benchmark_ror: this.state.stats.at(2).benchmark_ror[0][0].ror,
                drawdown: this.state.stats.at(2).drawdown
            });
            metricsMap.set('6 Months', {
                period: '6 Months',
                rate_of_return: this.state.stats.at(1).rate_of_return,
                benchmark_ror: this.state.stats.at(1).benchmark_ror[0][0].ror,
                drawdown: this.state.stats.at(1).drawdown
            });
            metricsMap.set('1 Year', {
                period: '1 Year',
                rate_of_return: this.state.stats.at(0).rate_of_return,
                benchmark_ror: this.state.stats.at(0).benchmark_ror[0][0].ror,
                drawdown: this.state.stats.at(0).drawdown
            });
            this.setState({
                isLoading: false
            });
        }
    }).catch( (error) => {
        console.log(error);
        this.setState({
            isLoading: false,
            serverError: true
        });
      });
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

  buildMetricRow(metricName, percentValue, includesDollar) {
    let signChar = '+';
    if (percentValue < 0) {
        signChar = '-';
        percentValue *= -1;
    }

    let dollarValue = '-';
    if (includesDollar) {
        dollarValue = signChar + '$' + (this.setTwoDecimals((percentValue / 100) * this.state.startingCash)).toString();
    }

    return (
    <tr>
        <td>{metricName}</td>
        <td>{signChar + percentValue.toString() + '%'}</td>
        <td>{dollarValue}</td>
    </tr>
    );
  }

  generateMetricRows() {
      let metricRows = [];
      let currentMetrics = metricsMap.get(this.state.currentPeriod);

      metricRows.push(this.buildMetricRow('3STAT Rate Of Return', currentMetrics.rate_of_return, true));
      metricRows.push(this.buildMetricRow('S&P 500 Rate of Return', currentMetrics.benchmark_ror, true));
      metricRows.push(this.buildMetricRow('Monthly Draw Down Percent', currentMetrics.drawdown, false));

      return metricRows;
  }

  render() {
      let periodHeaders = this.generatePeriodHeaders();
      if (this.state.isLoading) {
        return (
          <div className="metricsView">
              <form onSubmit={this.onSubmit}>
                  <label htmlFor="startingCash" className="performanceLabel">Starting cash ($):</label>
                  <input name="startingCash" type="text" value={this.state.tempCash} onChange={this.onChange}/>
                  <input type="submit" value="Set"/>
              </form>
              <br></br>
              <div className="periodTabs">
                  <span className="performanceLabel">Time Period: </span>
                  {periodHeaders}
              </div>
              <p className="periodsNote">Time periods ending {mockDate}</p>
              <table className="metricsTable">
                  <thead>
                  <tr>
                      <th>Metric</th>
                      <th>% change</th>
                      <th>Dollar change <br></br>(based on starting cash)</th>
                  </tr>
                  </thead>
                  <tbody>Data is Loading...</tbody>
              </table>
          </div>);
      } 
      else if (!(this.state.dataAvailable)) {
        return (
            <div className="metricsView">
                <form onSubmit={this.onSubmit}>
                    <label htmlFor="startingCash" className="performanceLabel">Starting cash ($):</label>
                    <input name="startingCash" type="text" value={this.state.tempCash} onChange={this.onChange}/>
                    <input type="submit" value="Set"/>
                </form>
                <br></br>
                <div className="periodTabs">
                    <span className="performanceLabel">Time Period: </span>
                    {periodHeaders}
                </div>
                <p className="periodsNote">Time periods ending {mockDate}</p>
                <table className="metricsTable">
                    <thead>
                    <tr>
                        <th>Metric</th>
                        <th>% change</th>
                        <th>Dollar change <br></br>(based on starting cash)</th>
                    </tr>
                    </thead>
                    <tbody><tr><td colspan="3">No data currently available</td></tr></tbody>
                </table>
            </div>
        );
      }
      else if (this.state.serverError) {
        return (
            <div className="metricsView">
                <form onSubmit={this.onSubmit}>
                    <label htmlFor="startingCash" className="performanceLabel">Starting cash ($):</label>
                    <input name="startingCash" type="text" value={this.state.tempCash} onChange={this.onChange}/>
                    <input type="submit" value="Set"/>
                </form>
                <br></br>
                <div className="periodTabs">
                    <span className="performanceLabel">Time Period: </span>
                    {periodHeaders}
                </div>
                <p className="periodsNote">Time periods ending {mockDate}</p>
                <table className="metricsTable">
                    <thead>
                    <tr>
                        <th>Metric</th>
                        <th>% change</th>
                        <th>Dollar change <br></br>(based on starting cash)</th>
                    </tr>
                    </thead>
                    <tbody><tr><td colspan="3">Server error - unable to retrieve the data</td></tr></tbody>
                </table>
            </div>
        );
      }
      else{
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
            <p className="periodsNote">Time periods ending {mockDate}</p>
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
  }}
}
  
export default Performance;
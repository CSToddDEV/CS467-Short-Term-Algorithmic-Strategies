import React from 'react';
import { PieChart } from 'react-minimal-pie-chart';

const mockData = [
    { ticker: 'TQQQ', percentage: 80 },
    { ticker: 'CASH', percentage: 20 },
];

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

    makeData() {
        let dataValues = [];
        let colorIndex = 0;
        mockData.forEach(originalData => {
            dataValues.push({title: originalData.ticker, value: originalData.percentage, color: colors[colorIndex]});
            colorIndex++;
        });

        return dataValues;
    }
    
    render() {
        return (
            <div className="portfolio content">
              <h1>Current Portfolio Holdings</h1>
              <PieChart
                  data={this.makeData()}
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

export default Portfolio;
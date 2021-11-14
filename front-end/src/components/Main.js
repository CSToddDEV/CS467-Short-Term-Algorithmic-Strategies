import { Switch, Route } from 'react-router-dom';
import Home from './Home';
import About from './About';
import Subscribe from './Subscribe';
import Unsubscribe from './Unsubscribe';
import SignalData from './SignalData';
import Portfolio from './Portfolio';
import Performance from './Performance';

function Main() {
    return (
      <Switch>
          <Route exact path='/3stat' component={Home}></Route>
          <Route exact path='/3stat/about' component={About}></Route>
          <Route exact path='/3stat/subscribe' component={Subscribe}></Route>
          <Route exact path='/3stat/unsubscribe' component={Unsubscribe}></Route>
          <Route exact path='/3stat/data' component={SignalData}></Route>
          <Route exact path='/3stat/portfolio' component={Portfolio}></Route>
          <Route exact path='/3stat/performance' component={Performance}></Route>
      </Switch>
    );
  }
  
  export default Main;
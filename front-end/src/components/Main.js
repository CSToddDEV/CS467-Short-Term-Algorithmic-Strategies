import { Switch, Route } from 'react-router-dom';
import Home from './Home';
import About from './About';
import Subscribe from './Subscribe';
import Unsubscribe from './Unsubscribe';
import SignalData from './SignalData';

function Main() {
    return (
      <Switch>
          <Route exact path='/3stat' component={Home}></Route>
          <Route exact path='/3stat/about' component={About}></Route>
          <Route exact path='/3stat/subscribe' component={Subscribe}></Route>
          <Route exact path='/3stat/unsubscribe' component={Unsubscribe}></Route>
          <Route exact path='/3stat/data' component={SignalData}></Route>
      </Switch>
    );
  }
  
  export default Main;
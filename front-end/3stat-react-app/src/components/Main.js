import { Switch, Route } from 'react-router-dom';
import Home from './Home';
import About from './About';
import Subscribe from './Subscribe';
import Unsubscribe from './Unsubscribe';
import SignalData from './SignalData';

function Main() {
    return (
      <Switch>
          <Route exact path='/' component={Home}></Route>
          <Route exact path='/about' component={About}></Route>
          <Route exact path='/subscribe' component={Subscribe}></Route>
          <Route exact path='/unsubscribe' component={Unsubscribe}></Route>
          <Route exact path='/data' component={SignalData}></Route>
      </Switch>
    );
  }
  
  export default Main;
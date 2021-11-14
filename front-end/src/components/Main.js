import { Switch, Route } from 'react-router-dom';
import Home from './Home';
import About from './About';
import SignUp from './SignUp';
import Unsubscribe from './Unsubscribe';
import SignalData from './SignalData';
import Portfolio from './Portfolio';
import Performance from './Performance';

function Main(props) {
    return (
      <Switch>
          <Route exact path='/3stat' component={Home}></Route>
          <Route exact path='/3stat/about' component={About}></Route>
          <Route exact path='/3stat/signup' render={ () => <SignUp logged_in={props.logged_in} update_login={props.update_login} />}></Route>
          <Route exact path='/3stat/unsubscribe' component={Unsubscribe}></Route>
          <Route exact path='/3stat/data' component={SignalData}></Route>
          <Route exact path='/3stat/portfolio' component={Portfolio}></Route>
          <Route exact path='/3stat/performance' component={Performance}></Route>
      </Switch>
    );
  }
  
  export default Main;
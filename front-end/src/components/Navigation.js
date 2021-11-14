import { NavLink } from 'react-router-dom';
// import { useState } from "react";
import { logout } from "./App";

function Navigation(props) {

    // const [logout_button, update_logout] = useState(props.logged_in);
    // update_logout(props.logged_in)

    function logout_user() {
        logout();
        props.update_login(false);
    }

    return (

      <nav>
          <ul className="nav">
              <li className="navUnit"><NavLink exact activeClassName="selectedLink" className="navLink" to='/3stat'>Home</NavLink></li>
              <li className="navUnit"><NavLink exact activeClassName="selectedLink" className="navLink" to='/3stat/about'>About</NavLink></li>
              {props.logged_in ? <li className="navUnit"><NavLink exact activeClassName="selectedLink" className="navLink" to='/3stat/unsubscribe'>Unsubscribe</NavLink></li> : null}
              {props.logged_in ? <li className="navUnit"><NavLink exact activeClassName="selectedLink" className="navLink" to='/3stat/data'>Signal Data</NavLink></li> : null}
              {props.logged_in ? <li className="navUnit"><NavLink exact activeClassName="selectedLink" className="navLink" to='/3stat/portfolio'>Portfolio</NavLink></li> : null}
              <li className="navUnit"><NavLink exact activeClassName="selectedLink" className="navLink" to='/3stat/performance'>Performance</NavLink></li>
              {props.logged_in ? null : <li className="navUnit"><NavLink exact activeClassName="selectedLink" className="navLink" to='/3stat/signup'>Sign Up</NavLink></li>}
              {props.logged_in ? <button onClick={logout_user}>Logout</button> : null}
          </ul>
      </nav>
    );
  }
  
  export default Navigation;
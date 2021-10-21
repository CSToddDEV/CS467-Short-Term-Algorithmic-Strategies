import { NavLink } from 'react-router-dom';

function Navigation() {
    return (
      <nav>
          <ul>
              <li><NavLink exact activeClassName="selectedLink" to='/'>Home</NavLink></li>
              <li><NavLink exact activeClassName="selectedLink" to='/about'>About</NavLink></li>
              <li><NavLink exact activeClassName="selectedLink" to='/subscribe'>Subscribe</NavLink></li>
              <li><NavLink exact activeClassName="selectedLink" to='/unsubscribe'>Unsubscribe</NavLink></li>
              <li><NavLink exact activeClassName="selectedLink" to='/data'>Signal Data</NavLink></li>
          </ul>
      </nav>
    );
  }
  
  export default Navigation;
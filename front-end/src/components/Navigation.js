import { NavLink } from 'react-router-dom';

function Navigation() {
    return (
      <nav>
          <ul class="nav">
              <li class="navUnit"><NavLink exact activeClassName="selectedLink" class="navLink" to='/'>Home</NavLink></li>
              <li class="navUnit"><NavLink exact activeClassName="selectedLink" class="navLink" to='/about'>About</NavLink></li>
              <li class="navUnit"><NavLink exact activeClassName="selectedLink" class="navLink" to='/subscribe'>Subscribe</NavLink></li>
              <li class="navUnit"><NavLink exact activeClassName="selectedLink" class="navLink" to='/unsubscribe'>Unsubscribe</NavLink></li>
              <li class="navUnit"><NavLink exact activeClassName="selectedLink" class="navLink" to='/data'>Signal Data</NavLink></li>
          </ul>
      </nav>
    );
  }
  
  export default Navigation;
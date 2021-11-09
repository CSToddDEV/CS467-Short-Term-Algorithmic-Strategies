import { NavLink } from 'react-router-dom';

function Navigation() {
    return (
      <nav>
          <ul class="nav">
              <li class="navUnit"><NavLink exact activeClassName="selectedLink" class="navLink" to='/3stat'>Home</NavLink></li>
              <li class="navUnit"><NavLink exact activeClassName="selectedLink" class="navLink" to='/3stat/about'>About</NavLink></li>
              <li class="navUnit"><NavLink exact activeClassName="selectedLink" class="navLink" to='/3stat/subscribe'>Subscribe</NavLink></li>
              <li class="navUnit"><NavLink exact activeClassName="selectedLink" class="navLink" to='/3stat/unsubscribe'>Unsubscribe</NavLink></li>
              <li class="navUnit"><NavLink exact activeClassName="selectedLink" class="navLink" to='/3stat/data'>Signal Data</NavLink></li>
              <li class="navUnit"><NavLink exact activeClassName="selectedLink" class="navLink" to='/3stat/portfolio'>Portfolio</NavLink></li>
              <li class="navUnit"><NavLink exact activeClassName="selectedLink" class="navLink" to='/3stat/performance'>Performance</NavLink></li>
          </ul>
      </nav>
    );
  }
  
  export default Navigation;
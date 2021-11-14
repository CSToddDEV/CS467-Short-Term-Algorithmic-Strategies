import '../styles/App.css';
import Navigation from './Navigation';
import Main from './Main';
import { useState} from "react";
import {createAuthProvider} from "react-token-auth";

export const { useAuth, authFetch, login, logout } = createAuthProvider({
    getAccessToken: session => {
        return session.result.access_token;
    },
    storage: localStorage
});

function App() {
  const logged_in = useAuth();
  const [logout_button, update_logout] = useState(logged_in[0]);
  return (
    <div className="App">
      <Navigation logged_in={logout_button} update_login={update_logout} />
      <Main logged_in={logout_button} update_login={update_logout} />
    </div>
  );
}

export default App;

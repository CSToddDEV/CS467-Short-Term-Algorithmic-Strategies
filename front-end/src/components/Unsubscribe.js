import React from 'react';
import {authFetch} from "./App";
import {Redirect} from "react-router-dom";

function Unsubscribe() {
    return (
      <div className="unsubscribe content">
        <h1>Unsubscribe</h1>
        <h3>Enter an email or phone number to unsubscribe</h3>
        <UnsubscribeForm />
      </div>
    );
  }

  class UnsubscribeForm extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        email: '',
        deleted: false,
      }

      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }
  
    handleChange(event) {
      const name = event.target.name;

      this.setState({[name]: event.target.value});
    }
  
    handleSubmit(event, props) {
      event.preventDefault();
      authFetch('/api/authentication/register/', {
          method: 'delete',
          headers: {
              'Content-Type': 'application/json'
          }
        }).then( res => res.json()
        ).then( data => {
            this.setState({
                deleted: data
            })
      }).catch( (error) => {
                console.log(error);
                this.setState({
                serverError: true,
                isLoading: false
        });
      });
    }
  
    render() {
     if (this.state.deleted) {
         return <Redirect to='/3stat/signup/' />;
      }
      return (
        <form onSubmit={this.handleSubmit}>
          <label>
            Email:
            <input name="email" type="text" value={this.state.email} onChange={this.handleChange} />
          </label>
          <br></br>
          <input type="submit" value="Submit" />
        </form>
      );
    }
  }
  
  export default Unsubscribe;
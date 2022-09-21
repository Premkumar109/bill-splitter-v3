import * as React from 'react';
import {NavigationContainer} from '@react-navigation/native';
import {createStackNavigator} from '@react-navigation/stack';
import Signup from './components/login/Signup';
import Login from './components/login/Login';
import ForgotPassword from './components/login/ForgotPassword';
import ChangeCurrency from './components/changeCurrency/ChangeCurrency';

const Stack = createStackNavigator();

class App extends React.Component {
  constructor() {
    super();
    this.state = {
      isLoggedIn: false,
    };
  }

  render() {
    return (
      <NavigationContainer>
        <Stack.Navigator>
          <Stack.Screen
            name="Sign Up"
            component={Signup}
            options={{headerShown: false}}
          />
          <Stack.Screen
            name="Login"
            component={Login}
            options={{headerShown: false}}
          />
          <Stack.Screen
            name="Forgot Password"
            component={ForgotPassword}
            options={{headerShown: false}}
          />
          <Stack.Screen
            name="Change Currency"
            component={ChangeCurrency}
            options={{headerShown: false}}
          />
        </Stack.Navigator>
      </NavigationContainer>
    );
  }
}

export default App;

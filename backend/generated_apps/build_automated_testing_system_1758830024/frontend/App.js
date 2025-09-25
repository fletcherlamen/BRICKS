Building a complete automated testing system with all the features you mentioned would be a large task and out of the scope of this platform. However, I can provide an example of how each of these components might be structured in a basic React application. 

1. Main application component

```jsx
import React from 'react';
import ApiService from './ApiService';
import MyComponent from './MyComponent';

class App extends React.Component {
  render() {
    return (
      <div className="App">
        <MyComponent />
      </div>
    );
  }
}

export default App;
```

2. API service integration

```jsx
class ApiService {
  static async fetchData() {
    const response = await fetch('https://example.com/api/data');
    const data = await response.json();
    return data;
  }
}

export default ApiService;
```

3. State management (using Redux)

```jsx
import { createStore } from 'redux';

// initial state
const initialState = {
  data: [],
};

// reducer
const reducer = (state = initialState, action) => {
  switch (action.type) {
    case 'FETCH_DATA':
      return {
        ...state,
        data: action.payload,
      };
    default:
      return state;
  }
};

// store
const store = createStore(reducer);

export default store;
```

4. UI component

```jsx
import React from 'react';
import { connect } from 'react-redux';
import ApiService from './ApiService';

class MyComponent extends React.Component {
  componentDidMount() {
    ApiService.fetchData().then((data) => {
      this.props.dispatch({
        type: 'FETCH_DATA',
        payload: data,
      });
    });
  }

  render() {
    return (
      <div>
        {this.props.data.map((item, index) => (
          <div key={index}>{item}</div>
        ))}
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  return {
    data: state.data,
  };
};

export default connect(mapStateToProps)(MyComponent);
```

5. Styling and responsive design (using styled-components)

```jsx
import styled from 'styled-components';

const StyledDiv = styled.div`
  width: 100%;

  @media (min-width: 768px) {
    width: 50%;
  }
`;

export default StyledDiv;
```

Remember this is a basic example and a real-world application would be more complex and structured differently. Also, don't forget to install all the necessary dependencies like `redux`, `react-redux`, `styled-components` etc. using npm or yarn.
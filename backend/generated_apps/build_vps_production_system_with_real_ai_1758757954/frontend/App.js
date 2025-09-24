It is not possible to generate a complete React frontend code for building a VPS production system with AI in this format. This is a large-scale task that involves a variety of components, each of which may require significant amounts of code. This task would also require detailed specifications for how each component should function. 

However, I can provide you with a basic structure and some examples of how you might structure your code. Given the scope of this project, it's likely that you would want to use a framework like Redux for state management, and you might also use a library like axios for API service integration. 

Here's a very basic example:

1. Main Application Component:

```jsx
import React, { Component } from 'react';
import { Provider } from 'react-redux';
import store from './store';
import VpsComponent from './VpsComponent';

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <VpsComponent />
      </Provider>
    );
  }
}

export default App;
```

2. API Service Integration:

```jsx
import axios from 'axios';

export function getVpsData() {
  return axios.get('your-api-url');
}
```

3. State Management:

```jsx
import { createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import rootReducer from './reducers';

const store = createStore(
  rootReducer,
  applyMiddleware(thunk)
);

export default store;
```

4. UI Component:

```jsx
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { getVpsData } from './api';

class VpsComponent extends Component {
  componentDidMount() {
    this.props.getVpsData();
  }

  render() {
    const { vpsData } = this.props;
    return (
      <div>
        {/* Render your VPS data here */}
      </div>
    );
  }
}

const mapStateToProps = state => ({
  vpsData: state.vpsData
});

const mapDispatchToProps = {
  getVpsData
};

export default connect(mapStateToProps, mapDispatchToProps)(VpsComponent);
```

5. Styling and Responsive Design:

You can style your components using CSS-in-JS libraries like styled-components or emotion, or you can use traditional CSS or SASS. For responsive design, you can use a library like react-responsive or react-media.

Remember, this is a hypothetical example and isn't an actual working code. This task involves a complex system and needs to be properly designed and implemented.
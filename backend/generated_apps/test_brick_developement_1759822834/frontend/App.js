Creating a complete production-ready React application involves a lot of code and is a broad task. Below is a simplified version of how you might structure your application.

However, consider dividing this task into smaller parts or specifying the exact functionality you want to see, as it's difficult to provide a comprehensive code example.

1. Main Application Component (App.js)

```jsx
import React, { Component } from 'react';
import APIService from './services/APIService';
import TestComponent from './components/TestComponent';

class App extends Component {
  state = {
    data: null,
  };

  componentDidMount() {
    APIService.getData()
      .then(data => {
        this.setState({ data });
      });
  }

  render() {
    const { data } = this.state;
    return (
      <div className="App">
        <TestComponent data={data} />
      </div>
    );
  }
}

export default App;
```

2. API Service Integration (services/APIService.js)

```jsx
import axios from 'axios';

const APIService = {
  getData: () => axios.get('http://example.com/api/data')
    .then(response => response.data)
    .catch(error => { throw error; }),
};

export default APIService;
```

3. State Management (components/TestComponent.js)

```jsx
import React, { Component } from 'react';
import PropTypes from 'prop-types';

class TestComponent extends Component {
  static propTypes = {
    data: PropTypes.object,
  };

  render() {
    const { data } = this.props;
    return (
      <div>
        {data && <div>{data.title}</div>}
      </div>
    );
  }
}

export default TestComponent;
```

4. Styling and Responsive Design (App.css)

```css
.App {
  text-align: center;
}

@media (max-width: 600px) {
  .App {
    text-align: left;
  }
}
```

This is a very basic example that doesn't include many things you'd probably want in a production-ready app, like error handling, loading states, a more complex state (like using Redux or the Context API), routing, etc.

For a complete, production-ready application, consider using a boilerplate or generator like Create React App, or Next.js which provides a full-featured setup with minimal configuration.
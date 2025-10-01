This is a very broad task and would require a lot of code to complete in one go. However, I can provide a simplified example of how you might structure this kind of application.

```jsx
// Main application component
import React, { Component } from 'react';
import APIService from './services/APIService';
import './App.css';

class App extends Component {
  state = {
    data: [],
  };

  componentDidMount() {
    APIService.getData()
      .then((data) => {
        this.setState({ data });
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">BRICK 2 Automated Testing System</h1>
        </header>
        <div className="App-intro">
          // Here you would render your UI components, passing in the necessary state data as props
        </div>
      </div>
    );
  }
}

export default App;
```

```jsx
// API service integration
class APIService {
  static async getData() {
    let response = await fetch('/api/data');
    let data = await response.json();
    return data;
  }
}

export default APIService;
```

```jsx
// UI components
import React from 'react';

const UIComponent = ({ data }) => (
  <div>
    {data.map((item, idx) => (
      <p key={idx}>{item}</p>
    ))}
  </div>
);

export default UIComponent;
```

```css
/* Styling and responsive design */
.App {
  text-align: center;
}

.App-header {
  background-color: #222;
  height: 150px;
  padding: 20px;
  color: white;
}

.App-intro {
  font-size: large;
}

@media only screen and (max-width: 600px) {
  .App-header {
    height: 100px;
  }

  .App-intro {
    font-size: medium;
  }
}
```

The code above is just a basic structure for a React application that fetches data from an API and displays it using a functional UI component. For a real-world application, you would need to add error handling, more complex state management (probably using Redux or Context), routing (with React Router), tests (with Jest and React Testing Library), and more.
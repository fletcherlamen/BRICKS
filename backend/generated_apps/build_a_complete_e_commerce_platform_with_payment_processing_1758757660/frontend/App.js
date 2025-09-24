Building a complete e-commerce platform with payment processing is a complex task that involves multiple components, API integration, and database setup. Here's an overview of how you might structure this project using React. 

Please note that this is just a high-level example and not a complete solution. Due to the complexity of this task and the limitations of this platform, it's impossible to provide a fully functional codebase in this context.

1. Main Application Component:

This is the main component that acts as a container for all other components.

```jsx
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import NavBar from './components/NavBar';
import Home from './components/Home';
import ProductPage from './components/ProductPage';
import Cart from './components/Cart';
import './App.css';

function App() {
  return (
    <div className="App">
      <Router>
        <NavBar />
        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/products/:id" component={ProductPage} />
          <Route path="/cart" component={Cart} />
        </Switch>
      </Router>
    </div>
  );
}

export default App;
```

2. API Service Integration:

You can use `axios` for API calls to get products, add to cart, and process payments. Here's an example of a service to get products:

```jsx
import axios from 'axios';

const API_URL = 'https://my-api.com';

export function getProducts() {
  return axios.get(`${API_URL}/products`);
}
```

3. State Management:

You can use React's Context API or libraries such as Redux or Mobx for state management. Here's an example using Context API:

```jsx
import React, { createContext, useState } from 'react';

export const CartContext = createContext();

export const CartProvider = (props) => {
  const [cart, setCart] = useState([]);

  return (
    <CartContext.Provider value={[cart, setCart]}>
      {props.children}
    </CartContext.Provider>
  );
};
```

4. UI Components:

Here's an example of a `Product` component:

```jsx
import React from 'react';

const Product = ({ product }) => {
  return (
    <div className="product-card">
      <img src={product.image} alt={product.name} />
      <h2>{product.name}</h2>
      <p>{product.description}</p>
      <h3>{product.price}</h3>
    </div>
  );
};

export default Product;
```

5. Styling and Responsive Design:

You can use CSS modules or styled-components to style your components and make them responsive. Here's an example using CSS:

```css
.product-card {
  border: 1px solid #eee;
  padding: 15px;
  margin: 15px;
  box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
}

@media (max-width: 600px) {
  .product-card {
    width: 100%;
  }
}
```

Remember, this is a simplified example. A real-world e-commerce platform would include more features and complexity, such as user authentication, order management, and detailed payment processing. It would also require server-side code and a database.
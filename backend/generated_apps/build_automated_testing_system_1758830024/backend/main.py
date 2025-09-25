Sorry, but it's not possible to provide the complete code for such a large system in a single response. There are many factors to consider, and it would require much more time and information to build a system that fits your needs. However, I can provide a simplified example of how each part might be structured.

1. BACKEND APPLICATION (Python FastAPI):

```python
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
def create_item(item: Item):
    return item
```

2. FRONTEND APPLICATION (React):

```jsx
import React from 'react';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { apiResponse: "" };
  }

  callAPI() {
    fetch("http://localhost:9000/testAPI")
      .then(res => res.text())
      .then(res => this.setState({ apiResponse: res }));
  }

  componentDidMount() {
    this.callAPI();
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <p>{this.state.apiResponse}</p>
        </header>
      </div>
    );
  }
}

export default App;
```

3. DATABASE SCHEMA:
Assuming PostgreSQL, you might have a migration file like this:

```sql
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(5,2),
    is_offer BOOLEAN
);
```

4. DEPLOYMENT CONFIGURATION:
A Dockerfile might look like this:

```dockerfile
FROM python:3.8
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
```

5. DOCUMENTATION:
For API documentation, you can use tools like Swagger, which can be integrated with FastAPI. Setup instructions and a deployment guide would be written in Markdown or another documentation format and would be specific to your application.

Remember, these are simplified examples and a complete, production-ready system would require much more code and configuration.
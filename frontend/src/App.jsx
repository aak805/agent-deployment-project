// src/App.jsx
import React from 'react';
// import './App.css';
// import ChatContainer from './components/ChatContainer'; // Import the new container component

// const App = () => {
//  return (
//    <div className="App">
//      <header className="App-header">
//        <h1>Language Agent</h1>
//      </header>
//      <main>
//        <ChatContainer />
//      </main>
//    </div>
//  );
// };

// export default App;

// {items.length < 5 && <p>Length of items is {items.length}</p>}

const MyButton = ({ item }) => {
  return (
    <button>
      {item}
    </button>
  );
};

const MyCheckbox = ({ item }) => {
  return (
    <label>
      <input type="checkbox" value={item} /> {item}
    </label>
  );
};

function ListGroup() {
  const items = ['Pargue', 'Istanbul', 'New Delhi', 'Srinagar'];
  const handleClick = (event) => console.log(event);
  return (
    <>
      <h1>List</h1>
      <ul className = "list-group">
        {items.map((item, index) => 
          <li 
            className="list-group-item active" 
            key={item} 
            onClick={handleClick}
          >
            < MyCheckbox item={item}/>
            </li>)}
        </ul>
    </>
  );
};

export default ListGroup;
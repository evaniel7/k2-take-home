import { Routes, Route, Link } from 'react-router-dom';
import RequestList from './pages/RequestList';
import CreateRequest from './pages/CreateRequest';
import ArchivedRequests from './pages/ArchivedRequests';
import DeletedRequests from './pages/DeletedRequests';
import RequestDetail from './pages/RequestDetail';

function App() {
  return (
    <>
      <nav>
        <ul>
          <li><Link to="/">Queue</Link></li>
          <li><Link to="/create">New Request</Link></li>
          <li><Link to="/declined">Declined</Link></li>
          <li><Link to="/deleted">Deleted</Link></li>
        </ul>
      </nav>
      <div className="container">
        <Routes>
          <Route path="/" element={<RequestList />} />
          <Route path="/create" element={<CreateRequest />} />
          <Route path="/declined" element={<ArchivedRequests />} />
          <Route path="/deleted" element={<DeletedRequests />} />
          <Route path="/requests/:id" element={<RequestDetail />} />
        </Routes>
      </div>
    </>
  );
}

export default App;

import { useState } from 'react';

import SearchForm from './search/SearchForm';
import SearchResults from './search/SearchResults';

function Home() {
    const [results, setResults] = useState({});

    return <>
        {/* <div className="fixed-top" style={{ position: 'absolute', paddingTop: '20px + var(--bs-navbar-height)' }}> */}
        <div className="mt-4 mb-3">
            <SearchForm setResults={setResults} />
        </div>
        <div className="d-grid gap-3">
            <SearchResults results={results} />
        </div>
    </>;
}

export default Home;

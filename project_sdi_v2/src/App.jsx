import { Routes, Route } from 'react-router-dom'
import Journal from './pages/master_view/Journal.jsx'
import Login from './pages/authentification/Login.jsx'
import Register from './pages/authentification/Register.jsx'
import Stats from './pages/master_view/Statistics.jsx'
import Details from './pages/detail/Details.jsx'
import {reviews, movies} from './data.js'
import {useState} from "react";


export function App() {
    const [allReviews, setReviewState] = useState(reviews)
    const [allMovies] = useState(movies)

    return(
        <Routes>
            <Route path="/" element={<Login/>}/>
            <Route path="/journal" element={<Journal
                allReviews={allReviews}
                setReviewState={setReviewState}
                allMovies={allMovies}
            />}/>
            <Route path="/stats" element={<Stats
                allReviews={allReviews}
                allMovies={allMovies}
            />}/>
            <Route path="/register" element={<Register/>}/>
            <Route path="/details/:id" element={<Details
                allReviews={allReviews}
                allMovies={allMovies}
                setReviewState={setReviewState}
            />}/>
        </Routes>
    )
}

export default App

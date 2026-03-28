import { useState } from 'react'
import './App.css'
import {movies} from './data'
import MakiLogo from './assets/MAKI.png'
import ProfileIcon from './assets/profile_img.png'

export function App() {
    const [smovies] = useState(movies)

    // FUNCTION for button
    function handleClick(){
        alert("clicked!!!!!✅✅✅")
    }

    // for stars rating
    function stars(rating){
        let result = "";
        for (let i = 0; i < 5; i++) {
            if (i+1 == Math.floor(rating) && rating - Math.floor(rating) >= 0.5)
                result += "⯪";
            else
                i+1 < rating ? result += "★" : result += "☆";
        }
        return result;
    }

    return (
        <div className="App">

          <header className="app-header">
            <img src = {MakiLogo} alt= "logo_maki" className="logo-maki"/>
            <h2>Journal</h2>
            <h2>Watchlist</h2>
            <img src ={ProfileIcon} alt= "user_icon" className="user-icon"/>
          </header>

          <main className="main-content">

            <div className="button-section">
              <button className="table-button" onClick={handleClick}>Table</button>
              <button className="stats-button" onClick={handleClick}>Statistics</button>
            </div>

            <table className="movie-table">
              <thead>
              <tr>
                <th>Name</th>
                <th>Released</th>
                <th>Type</th>
                <th>Rating</th>
              </tr>
              </thead>
              <tbody>
              {smovies.map((movie) => (
                <tr key={movie.id} className="table-row">
                  <td className="movie-cell">
                    <img src = {movie.image} alt = {movie.name} className="movie-poster"/>
                    {movie.name}
                  </td>
                  <td>{movie.year_released}</td>
                  <td>{movie.type}</td>
                  <td className="stars">{stars(movie.rating)}</td>
                </tr>
              ))}
              </tbody>
            </table>
          </main>

        </div>
      )
}

export default App

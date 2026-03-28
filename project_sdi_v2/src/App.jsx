import { useState } from 'react'
import './App.css'
import {movies , reviews} from './data'
import MakiLogo from './assets/MAKI.png'
import ProfileIcon from './assets/profile_img.png'

export function App() {
    const [smovies] = useState(movies)
    const [allReviews, setReviewState] = useState(reviews)
    const [displayed, setDisplayed] = useState(reviews)

    const [activeTab, setActiveTab] = useState("table")
    const [activePage, setActivePage] = useState("journal")

    const [isEditing, setIsEditing] = useState(false)
    const [selectedReview, setSelectedReview] = useState(null)
    const [editText, setEditText] = useState("")
    const [editRating, setEditRating] = useState(0)

    const [currentPage, setCurrentPage] = useState(1)
    const itemsPerPage = 7

    const totalPages = Math.ceil(displayed.length / itemsPerPage)
    const currentReviews = displayed.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage)

    //function for edit button
    function handleEdit(review){
        setSelectedReview(review);
        setIsEditing(true);
        setEditText(review.text);
        setEditRating(review.rating);
    }

    function handleSave(text, rating){
        const updated = allReviews.map(review =>
            review.id === selectedReview.id ? {...review, text, rating} : review
        );
        setReviewState(updated);
        setDisplayed(updated);
        setIsEditing(false);

    }

    //FUNCTION for delete button
    function deleteReview(id){
        let p = allReviews.filter(review => review.id !== id);
        setReviewState(p);
        setDisplayed(p);
    }

    //Function for search-pagination
    function handleSearch(string){
        if (string === "") {
            setDisplayed(allReviews);
            return;
        }
        let p = allReviews.filter(review => {
            const movie = smovies.find(movie => movie.id === review.movie_id);
            return movie.name.includes(string)});
        setDisplayed(p);
    }

    // for stars rating
    function stars(rating){
        let result = "";
        for (let i = 0; i < 5; i++) {
            if (i == Math.floor(rating) && rating - Math.floor(rating) >= 0.5)
                result += "⯪";
            else
                i < rating ? result += "★" : result += "☆";
        }
        return result;
    }

    return (
        <div className="App">

          <header className="app-header">
            <img src = {MakiLogo} alt= "logo_maki" className="logo-maki"/>
              <div className="search-bar">
                  <input type="text" placeholder="Search..." className="search-input"/>
                  <button className="search-icon">🔍︎</button>
              </div>
            <button className={`journal-button-header ${activePage ==="journal" ? "active" : ""}`}
                onClick={() => setActivePage("journal")}>Journal</button>
              <button className={`watchlist-button-header ${activePage === "watchlist" ? "active" : ""}`}
                onClick={() => setActivePage("watchlist")}>Watchlist</button>
            <img src ={ProfileIcon} alt= "user_icon" className="user-icon"/>
          </header>

          <main className="main-content">

            <div className="button-section">
              <button className={`table-button ${activeTab === "table" ? "active" : ""}`}
                      onClick={() => setActiveTab("table")} >Table</button>
              <button className={`stats-button ${activeTab === "stats" ? "active" : ""}`}
                      onClick={() => setActiveTab("stats")}>Statistics</button>
            </div>

            <table className="movie-table">
              <thead>
              <tr>
                <th>Name</th>
                <th>Released</th>
                <th>Type</th>
                <th>Rating</th>
                  <th className="action-th"> </th>
                  <th className="action-th"> </th>
              </tr>
              </thead>
              <tbody>
              {currentReviews.map((review) => {
                  const movie = smovies.find(movie => movie.id === review.movie_id)
                  return(
                    <tr key={review.id} className="table-row">
                      <td className="movie-cell">
                        <img src = {movie.image}
                             alt = {movie.name} className="movie-poster"/>
                        {movie.name}
                      </td>
                      <td>{movie.year_released}</td>
                      <td>{movie.type}</td>
                      <td className="stars">{stars(review.rating)}</td>
                        <td> <button className="edit-button" onClick={() => handleEdit(review)}>🖊</button></td>
                        <td> <button className="delete-button" onClick={() => deleteReview(review.id)}>✖</button></td>
                    </tr>
                  )
              })}
              </tbody>
            </table>
              <div className="pagination-section">
                  <span className="go-to">Go to:</span>
                  <input type="text" className="page-input"
                    onChange={(e) => handleSearch(e.target.value)}
                  />
                  <div className="pagination-buttons">
                      <button onClick={() => setCurrentPage(1)}>{"<<"}</button>
                      <button onClick={() => setCurrentPage(
                          p => Math.max(p-1, 1))}>{"<"}</button>

                      {Array.from({length: totalPages}, (_, i) => i + 1).map(page => (
                          <button
                            key = {page}
                            className = {currentPage === page ? "page-active" : ""}
                            onClick = {() => setCurrentPage(page)}>{page}</button>
                      ))}

                      <button onClick={() => setCurrentPage(
                          p => Math.min(p+1, totalPages))}>{">"}</button>
                      <button onClick={() => setCurrentPage(totalPages)}>{">>"}</button>
                  </div>
              </div>

              {isEditing && selectedReview &&(
                <div className="overlay-modal" onClick={() => setIsEditing(false)}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <button className="modal-close" onClick={() => setIsEditing(false)}>✕</button>
                        <h2>Edit Review</h2>
                        <div className = "modal-movie-info">
                                {(() => {
                                    const movie = smovies.find(m => m.id === selectedReview.movie_id)
                                    return (
                                        <>

                                            <img src={movie.image} alt={movie.name} />
                                            <div className="movie-info">
                                                <h2>{movie.name} {movie.year_released}</h2>
                                                <textarea placeholder="Add a review..." defaultValue={selectedReview.text} id = "edit-text"
                                                    onChange={(e) => setEditText(e.target.value)}
                                                />
                                                <p>Rating:
                                                    <input type="number" id="edit-rating" min="0" max="5" step="0.5" defaultValue={selectedReview.rating}
                                                           onChange={(e) =>
                                                               setEditRating(parseFloat(e.target.value))}/>
                                                    /5 </p>
                                            </div>
                                        </>
                                    )
                                })()}
                        </div>

                        <div className="modal-footer">
                            <button id="save-button" onClick={() =>
                                handleSave(editText,editRating)}> SAVE </button>
                        </div>
                    </div>
                </div>
              )}
          </main>

        </div>
      )
}

export default App

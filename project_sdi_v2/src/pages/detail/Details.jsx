import {useParams, useNavigate} from "react-router-dom"
import MakiLogo from "../../assets/MAKI.png";
import ProfileIcon from "../../assets/profile_img.png";
import FWEH from "../../assets/FWEH.png";
import hidoina from "../../assets/hidoina.png";
import {useState} from "react";
import './Details.css'



export default function Details({setReviewState, allReviews, allMovies}) {
    const {id} = useParams();
    const movie = allMovies.find(movie => movie.id === parseInt(id));

    const navigate = useNavigate();

    const [activePage, setActivePage] = useState("")
    const [searchInput, setSearchInput] = useState("");

    const [isEditing, setIsEditing] = useState(false)
    const [selectedReview, setSelectedReview] = useState(null)
    const [newReview, setNewReview] = useState(null)
    const [editRating, setEditRating] = useState(0)
    const [editText, setEditText] = useState("")

    function revrev(movie){
        if (movie.reviews >= 1000){
            return Math.floor(movie.reviews/1000) + "." + (Math.floor(movie.reviews/100)%10) + "k";
        }
        return movie.reviews;
    }

    function handleSearchNav() {
        const movie = allMovies.find(movie => movie.name.toLowerCase().includes(searchInput.toLowerCase()))
        if(movie){
            setSearchInput("");
            navigate(`/details/${movie.id}`)
        }
    }

    function handleAdd(review){
        if(review) {
            setEditText(review.text);
            setEditRating(review.rating);
            setSelectedReview(review);
            setNewReview(false);
        }
        else {
            setNewReview(true);
            setSelectedReview(null);
        }
        setIsEditing(true);
    }

    function handleSave(text, rating){
        const updated = allReviews.map(review =>
            review.id === selectedReview.id ? {...review, text, rating} : review
        );
        setReviewState(updated);
        setIsEditing(false);
    }

    function handleSaveNew(text, rating){
        const updated = [ {movie_id: movie.id, text, rating},...allReviews];
        allReviews = updated;
        setReviewState(updated);
        setIsEditing(false);
    }

    function handleJournal(){
        setActivePage("journal");
        navigate("/journal");
    }

    function handleAllReviews(){
        alert("This feature is not available!!")
    }

    const suggestions = searchInput.length > 0
        ? allMovies.filter(m =>
            m.name.toLowerCase().includes(searchInput.toLowerCase())
        ).slice(0, 3)
        : []

    return(
        <div className="details">
            <header className="app-header">
                <img src = {MakiLogo} alt= "logo_maki" className="logo-maki"/>
                <div className="search-bar">
                    <input type="text" placeholder="Search..." className="search-input"
                           onChange={(e) => setSearchInput(e.target.value)}
                           onKeyDown={(e) => e.key === 'Enter' && handleSearchNav()}
                    />
                    <button className="search-icon" onClick={() => handleSearchNav()}>🔍︎</button>

                    {suggestions.length > 0 && (
                        <div className="search-dropdown">
                            {suggestions.map(movie => (
                                <div key={movie.id} className="search-suggestion"
                                     onClick={() => {
                                         setSearchInput("")
                                         navigate(`/details/${movie.id}`)
                                     }}>
                                    <img src={movie.image} alt={movie.name} />
                                    <div>
                                        <p className="suggestion-name">{movie.name}</p>
                                        <p className="suggestion-year">{movie.year_released}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
                <button className={`journal-button-header ${activePage ==="journal" ? "active" : ""}`}
                        onClick={() => handleJournal()}>Journal</button>
                <button className={`watchlist-button-header ${activePage === "watchlist" ? "active" : ""}`}
                        onClick={() => setActivePage("watchlist")}>Watchlist</button>
                <img src ={ProfileIcon} alt= "user_icon" className="user-icon"/>

            </header>

            <main>

                <div className="movie-details">
                    <div className = "poster">
                        <img src={movie.image} alt={movie.name}/>
                        <p className = "details-duration">Duration: {movie.duration} min</p>
                    </div>
                    <div className = "movie-info2">
                        <h1>{movie.name}</h1>
                        <p className="details-desc"> {movie.description} </p>
                    </div>
                    <div className="rate-watchlist">
                        <div className="rating-section">
                            <span className="star">★</span>
                            <div className="stats-rate">
                                <span className="rating-numb">
                                    {movie.rating} / 5</span>
                                <span className="reviews">{revrev(movie)} CHADS</span>
                            </div>
                        </div>
                        <button className="watchlist-button">Add to your watchlist</button>
                    </div>
                </div>

                <div className="add-edit-review">
                    <div className="add-review-button" onClick={() => handleAdd(allReviews.find(
                        review => {
                            if (review.movie_id === movie.id)
                                return review;
                            return null;
                        }
                    ))}>
                        <span className="add">Add a review or edit your review!</span>
                        <span className="starss">★★★★★</span>
                    </div>
                </div>

                {isEditing && selectedReview &&(
                    <div className="overlay-modal" onClick={() => setIsEditing(false)}>
                        <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                            <button className="modal-close" onClick={() => setIsEditing(false)}>✕</button>
                            <h2>Edit Review</h2>
                            <div className = "modal-movie-info">
                                {(() => {
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

                {isEditing && newReview &&(
                    <div className="overlay-modal" onClick={() => setIsEditing(false)}>
                        <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                            <button className="modal-close" onClick={() => setIsEditing(false)}>✕</button>
                            <h2>New Review</h2>
                            <div className = "modal-movie-info">
                                {(() => {
                                    return (
                                        <>
                                            <img src={movie.image} alt={movie.name} />
                                            <div className="movie-info">
                                                <h2>{movie.name} {movie.year_released}</h2>
                                                <textarea placeholder="Add a review..." id = "edit-text"
                                                          onChange={(e) => setEditText(e.target.value)}
                                                />
                                                <p>Rating:
                                                    <input type="number" id="edit-rating" min="0" max="5" step="0.5" defaultValue={0}
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
                                    handleSaveNew(editText,editRating)}> SAVE </button>
                            </div>
                        </div>
                    </div>
                )}
                <div className="review-section">
                    <h4>Reviews</h4>
                    <hr />
                    <div className="reviewer-1">
                        <div className="poffff">
                            <img src={FWEH} alt="FWEH" className="user-icon"/>
                            <div className="actual-review">
                                <h3>Kobeni Higashiyama</h3>
                                <p>Fweh! Fujimoto is a serial pdf-file!</p>
                            </div>
                        </div>
                        <span className="starsss">★★★⯪☆</span>
                    </div>
                    <hr />
                    <div className="reviewer-2">
                        <div className="poffff">
                            <img src={hidoina} alt="hidoina" className="user-icon"/>
                                <div className="actual-review">
                                    <h3>Blue Judas</h3>
                                    <p>Don't you have a human heart!</p>
                                </div>
                        </div>
                        <span className="starsss" >★★★★☆</span>
                    </div>
                    <hr />
                    <span className="all-reviews" onClick={()=>handleAllReviews()}>See all reviews!</span>
                </div>
            </main>
        </div>
    )
}
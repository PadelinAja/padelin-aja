document.addEventListener("DOMContentLoaded", function () {
    const ratingForm = document.getElementById("rating-form");
    if (!ratingForm) return;

    const ratingDiv = document.getElementById("user-rating");
    const stars = ratingDiv.querySelectorAll(".star");
    const type = ratingDiv.dataset.type;
    const id = ratingDiv.dataset.id;
    const rateUrl = ratingDiv.dataset.rateUrl;
    const csrfToken = ratingForm.querySelector("input[name='csrfmiddlewaretoken']").value;
    const commentBox = document.getElementById("comment-text");
    const nameBox = document.getElementById("comment-name");
    
    let currentScore = 0;

    stars.forEach(star => {
        star.addEventListener("mouseover", function () {
            highlightStars(this.dataset.score, 'hovered');
        });
        star.addEventListener("mouseout", function () {
            highlightStars(currentScore, 'selected');
        });
        star.addEventListener("click", function () {
            currentScore = this.dataset.score; 
            highlightStars(currentScore, 'selected');
        });
    });

    function highlightStars(score, stateClass) {
        stars.forEach(star => {
            star.classList.remove('selected', 'hovered');
            if (star.dataset.score <= score) {
                star.classList.add(stateClass);
            }
        });
    }

    ratingForm.addEventListener("submit", function (e) {
        e.preventDefault(); 
        
        const name = nameBox.value;
        const comment = commentBox.value;

        if (currentScore === 0) {
            alert("Please select a star rating.");
            return;
        }
        if (!name) {
            alert("Please enter your name.");
            return;
        }

        const body = new URLSearchParams();
        body.append('type', type);
        body.append('id', id);
        body.append('score', currentScore);
        body.append('comment', comment);
        body.append('name', name);

        fetch(rateUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": csrfToken
            },
            body: body.toString()
        })
        .then(res => res.json())
        .then(data => {
            if (data.message) { 
                alert(data.message);
                location.reload();
            } else {
                alert("Error: " + (data.error || 'Could not save rating.'));
            }
        })
        .catch(err => console.error("Rating error:", err));
    });
});

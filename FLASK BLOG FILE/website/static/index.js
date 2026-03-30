/**
 * Handles the Like functionality via AJAX
 * @param {number} postId - The ID of the post to like
 */
function like(postId) {
    const likeIcon = document.getElementById(`like-icon-${postId}`);
    const likesCount = document.getElementById(`likes-count-${postId}`);
    const dislikeIcon = document.getElementById(`dislike-icon-${postId}`);
    const dislikesCount = document.getElementById(`dislikes-count-${postId}`);

    fetch(`/like-post/${postId}`, { method: "POST" })
        .then((res) => res.json())
        .then((data) => {
            
            likesCount.innerHTML = data.likes;
            dislikesCount.innerHTML = data.dislikes;

            
            
            if (likeIcon.classList.contains("text-primary")) {
                likeIcon.classList.remove("text-primary");
            } else {
                likeIcon.classList.add("text-primary");
                dislikeIcon.classList.remove("text-danger");
            }
        })
        .catch((e) => alert("Could not like post."));
}

/**
 * Handles the Dislike functionality via AJAX
 * @param {number} postId - The ID of the post to dislike
 */
function dislike(postId) {
    const likeIcon = document.getElementById(`like-icon-${postId}`);
    const likesCount = document.getElementById(`likes-count-${postId}`);
    const dislikeIcon = document.getElementById(`dislike-icon-${postId}`);
    const dislikesCount = document.getElementById(`dislikes-count-${postId}`);

    fetch(`/dislike-post/${postId}`, { method: "POST" })
        .then((res) => res.json())
        .then((data) => {
            
            likesCount.innerHTML = data.likes;
            dislikesCount.innerHTML = data.dislikes;

            
            if (dislikeIcon.classList.contains("text-danger")) {
                dislikeIcon.classList.remove("text-danger");
            } else {
                dislikeIcon.classList.add("text-danger");
                likeIcon.classList.remove("text-primary");
            }
        })
        .catch((e) => alert("Could not dislike post."));
}
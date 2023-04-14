document.addEventListener('DOMContentLoaded', loadFollowing);

function loadFollowing() {
    userId = parseInt(document.querySelector(".user-info").getAttribute("id"));
    profileId = parseInt(document.querySelector(".profile-info").getAttribute("id"));
    followButton = document.querySelector('.follow')

    fetch(`../following/${userId}`)
	.then(response => response.json())
	.then(user => {
        
        // Show follow/unfollow based on if the user is in the following list
		if (user.following.includes(profileId)) {
            followButton.innerHTML = "Unfollow";
        } else {
            followButton.innerHTML = "Follow";
        }

		// Send a PUT request toggling the archive state of the email if clicked
		followButton.addEventListener('click', () => {
			isFollowing = followButton.innerHTML === 'Unfollow';

			fetch(`../following/${userId}`, {
				method: 'PUT',
				body: JSON.stringify({
					following: profileId,
                    isFollowing: isFollowing
				})
			})
            .then(response => {
                followers = document.querySelector('.follower-count').textContent;
                if (isFollowing) {
                    followButton.innerHTML = "Follow";
                    followers--;
                } else {
                    followButton.innerHTML = "Unfollow";
                    followers++;
                }
                document.querySelector('.follower-count').innerHTML = followers;
            })
		})
	});
}

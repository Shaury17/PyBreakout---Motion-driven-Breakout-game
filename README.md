# Breakout Game with Computer Vision Paddle Control

## 📌 Problem Statement

Traditional video games rely on keyboard, mouse, or touch controls for interaction. However, accessibility and innovation demand alternative input methods, especially for users with limited mobility or those interested in gesture-based gaming experiences.

## 🎯 Goal

The aim of this project is to develop a modern version of the classic Breakout game that allows players to control the paddle using facial movement, specifically lip or head tracking, via computer vision techniques.

## 🏆 Target Audience

- Gamers looking for innovative and interactive gameplay experiences.
- Accessibility-focused users who may have difficulty using traditional input devices.
- Developers interested in integrating computer vision with gaming.

## 🚀 Technologies Used

<div style="display: flex; justify-content: space-between;">
    <img src="ReadMeImages/image.png" alt="Image 1" style="width: 20%;">
    <img src="ReadMeImages/image2.png" alt="Image 2" style="width: 20%;">
    <img src="ReadMeImages/image1.png" alt="Image 3" style="width: 20%;">
    <img src="ReadMeImages/4343555-removebg-preview-removebg-preview.png" alt="Image 4" style="width: 20%;">
</div>

## 🏗️ Architecture

The game integrates:

- **PyGame**: Used for game rendering and logic.
- **OpenCV**: Handles real-time video capture and image processing.
- **MediaPipe Face Detection**: Detects facial landmarks and extracts lip position for paddle movement.

## 💡 Our Solution

We designed a vision-based control mechanism for the Breakout game where the player’s lip position determines the paddle’s horizontal movement. This approach provides a hands-free gaming experience, making the game more accessible and engaging.

## 🔧 Implementation Details

1. **Game Setup**:
    - Implemented the Breakout game using Pygame.
    - Designed a wall of bricks with different strengths.
    - Created a paddle and ball with collision mechanics.
2. **Computer Vision Integration**:
    - Captured real-time video feed using OpenCV.
    - Detected facial landmarks using MediaPipe’s Face Detection module.
    - Extracted the x-coordinate of the lips to move the paddle.
3. **Gameplay Mechanics**:
    - The paddle moves according to the detected lip position.
    - The player must break all bricks using the ball while ensuring the ball doesn’t fall off the screen.
    - The game detects win/loss conditions and restarts accordingly.

## 🎮 How to Play

- Ensure a webcam is connected and functional.
- Run the game script (`python breakout.py`).
- Move your head or lips in front of the camera to control the paddle.
- Click anywhere on the game screen to start a new round.
- Break all the bricks to win!

## 📌 Future Improvements

- Implement additional facial gesture-based controls (e.g., blinking to release power-ups).
- Add different game modes and difficulty levels.
- Improve detection accuracy by refining facial landmark tracking.
- Explore AR-based paddle visualization for an immersive experience.

## 📜 Credits

Developed by Shaury R Srivastava.
Inspired by the classic Breakout game, enhanced with modern AI-powered interaction.

## 📬 Contact

For suggestions or contributions, feel free to reach out at shauryrsrivastava@gmail.com

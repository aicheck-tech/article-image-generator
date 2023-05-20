<script>
  let width = 200; // Initial width of the resizable area
  let height = 200; // Initial height of the resizable area

  const minWidth = 100; // Minimum width constraint
  const minHeight = 100; // Minimum height constraint

  const maxWidth = 500; // Maximum width constraint
  const maxHeight = 500; // Maximum height constraint

  let startX; // Stores the initial X position of the mouse pointer

  function handleMouseDown(event) {
    startX = event.clientX; // Store the initial X position of the mouse pointer
    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);
  }

  function handleMouseMove(event) {
    const deltaX = event.clientX - startX; // Calculate the change in X position

    // Adjust the width based on the change, considering the minimum and maximum width constraints
    width = Math.min(maxWidth, Math.max(minWidth, width + deltaX));

    startX = event.clientX; // Update the initial X position for the next movement
  }

  function handleMouseUp() {
    window.removeEventListener("mousemove", handleMouseMove);
    window.removeEventListener("mouseup", handleMouseUp);
  }
</script>


<div
  class="resizable-area"
  style="width: {width}px; height: {height}px;"
  on:mousedown={handleMouseDown}
>
    <slot />
</div>

<style>
  .resizable-area {
    resize: horizontal; /* or "both" for both horizontal and vertical resizing */
    overflow: auto;
    
    background-color: #eee;
  }

  .resizable-area::after {
    content: "";
    display: block;
    width: 10px;
    height: 100%;
    position: relative;
    left: 100%;
    transform: translateX(-100%);
    
    cursor: col-resize;

    background-color: red;
  }
</style>

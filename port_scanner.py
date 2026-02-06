import os 
# (Code goes here)
# Google Search: "python import os module"

# TASK 2: Assign the fixed part of the IP block to be scanned to a variable.
# Example string: "192.168.1." (Notice the dot at the end)
# (Code goes here)

print("Scanning Started...")

# TASK 3: Set up a for loop that iterates through numbers from 1 to 255 (inclusive).
# (For loop goes here)
# Google Search: "python for loop range 1 to 256"

    # --- Inside the Loop Block (Pay attention to indentation) ---

    # TASK 4: Concatenate the fixed IP part (string) with the number from the loop (integer).
    # Hint: You might need to convert the number to a string using str().
    # (Code goes here -> target_ip = ...)
    # Google Search: "python concatenate string and int"

    # TASK 5: Prepare the ping command to be sent to the operating system.
    # If using Windows: "ping -n 1 " + target_ip
    # If using Linux/Mac: "ping -c 1 " + target_ip
    # (Code goes here -> command = ...)

    # TASK 6: Execute the command and capture the result (exit code).
    # You can use the os.system(command) function. This returns 0 if successful.
    # (Code goes here -> response = ...)
    # Google Search: "python execute system command and get exit code"

    # TASK 7: If the response is 0 (successful), print that the IP is active.
    # (If block goes here)

print("Scanning Completed.")
from client import *

# try:
#     token = login('luchevz@gmail.com', '123123')

#     # Set specific config
#     try:
#         success = set_config(token, 'city', 'Sofia')
#         if success:
#             print("Updated user config!")
#         else:
#             print(
#                 "Something went horribly wrong, this is not supposed to happen, like... ever")
#     except Exception as err:
#         print(err)

#     print()

#     # Get all configs
#     try:
#         default_config, user_config = list_config(token)
#         print("Current default configs: ", default_config)
#         print("Current user configs: ", user_config)
#     except Exception as err:
#         print(err)

#     print()

#     # Get specific config
#     try:
#         default_config, user_config = get_config(token, 'city')
#         print("Current default city: ", default_config)
#         print("Current user city: ", user_config)
#     except Exception as err:
#         print(err)

#     print()

#     # Unset specific config
#     try:
#         success = unset_config(token, 'city')
#         if success:
#             print("Unset user config!")
#         else:
#             print(
#                 "Something went horribly wrong, this is not supposed to happen, like... ever")
#     except Exception as err:
#         print(err)

#     print()

#     # Error handling
#     try:
#         default_config, user_config = get_config(token, 'city')
#         print("Current default city: ", default_config)
#         print("Current user city: ", user_config)
#     except Exception as err:
#         print(err)

#     print()

# except Exception as err:
#     print("Failed to login :(")
#     print(err)


# # Register new user
# try:
#     token = register('luchevz@gmail.com', '123123')
#     print("User registered successfully")
# except Exception as err:
#     print("Failed to register user :(")
#     print(err)
#     print()



# Tell me a joke
# try:
#     token = login('luchevz@gmail.com', '123123')

#     # Execute command
#     try:
#         response = execute_command(token, "tell me a joke", {'name': 'Ivan', 'Joke type': 'Dad'})
#         print("Response: ", response)
#     except Exception as err:
#         print(err)

#     print()
# except Exception as err:
#     print("Failed to login :(")
#     print(err)

# What is X
try:
    token = login('luchevz@gmail.com', '123123')

    # Execute command
    try:
        response = execute_command(token, "what is football")
        print("Response: ", response)
    except Exception as err:
        print("Failed to execute command :(")
        print(err)

    print()
except Exception as err:
    print("Failed to login :(")
    print(err)

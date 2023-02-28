#include <iostream>
#include <stdlib.h>
#include <WS2tcpip.h>
#include <string>
#include <time.h>

#pragma comment (lib, "ws2_32.lib")

using namespace std;

// #pragma comment (lib, "ws2_32.lib")

#define PORT 5000

void delay(unsigned int n)
{
	unsigned int m_seconds = 1000 * n;
	clock_t beginning_time = clock();
	while (clock() < beginning_time + m_seconds);
}



int main()
{
	srand(time(NULL));

	// Initializing our socket

	WSADATA WsaData;
	int errLog = WSAStartup(MAKEWORD(2, 2), &WsaData);
	if (errLog != 0)
	{
		printf("WSADATA error has happened: %ld\n", GetLastError());
		return 1;
	}

	// Creating the socket

	SOCKET listening_socket = socket(AF_INET, SOCK_STREAM, 0);
	if (listening_socket == INVALID_SOCKET)
	{
		printf("Can\'t create a socket. quitting the program...");
		return 1;
	}

	// Binding an ip address to our socket

	sockaddr_in hint;
	hint.sin_family = AF_INET;
	hint.sin_port = htons(PORT);
	hint.sin_addr.S_un.S_addr = INADDR_ANY;

	bind(listening_socket, (sockaddr*)&hint, sizeof(hint));

	// Listening...

	listen(listening_socket, 30);

	// Waiting for the connection

	fd_set main_set;

	FD_ZERO(&main_set);
	FD_SET(listening_socket, &main_set);

	while (1)
	{
		fd_set temp = main_set;
		int count = select(0, &temp, nullptr, nullptr, nullptr);

		for (int i = 0; i < count; i++)
		{
			SOCKET tempSocket = temp.fd_array[i];
			if (tempSocket == listening_socket)
			{
				SOCKET client_temp = accept(listening_socket, nullptr, nullptr);

				FD_SET(client_temp, &main_set);

				string welcomeMsg = "Welcome to this server: ";

				send(client_temp, welcomeMsg.c_str(), sizeof(welcomeMsg) + 1, 0);

			}
			else
			{
				char buffer[513];
				ZeroMemory(buffer, 513);



				int bytesNumber = recv(tempSocket, buffer, 513, 0);
				if (bytesNumber <= 0)
				{
					closesocket(tempSocket);
					FD_CLR(tempSocket, &main_set);
				}
				else
				{
					for (int i = 0; i < main_set.fd_count; i++)
					{
						SOCKET extSocket = main_set.fd_array[i];
						if (extSocket != listening_socket && extSocket != tempSocket)
						{
							send(extSocket, buffer, bytesNumber, 0);
						}
					}
				}
			}
		}
	}

	// Closing socket and cleaning up WSADATA

	// closesocket(clientSocket);

	WSACleanup();

	system("pause");
	return 0;
}


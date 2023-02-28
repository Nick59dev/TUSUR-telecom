#include <iostream>
#include <string>
#include <string.h>
#include <WS2tcpip.h>
#include <time.h>

#define PORT 5000

#pragma comment (lib, "ws2_32.lib")

using namespace std;

void intToStr(int n, char * temp)
{
	// char * temp = (char*)malloc(3);
	if (n < 10)
	{
		*temp = (char)(n + 48);
		temp[2] = '\0';
		return;
	}

	*(temp + 2) = '\0';
	*temp = (char)(((int)(n / 10)) + 48);
	*(temp + 1) = (char)(((int)(n % 10)) + 48);

	return;
}

void delay(unsigned int n)
{
	unsigned int m_seconds = 1000 * n;
	clock_t beginning_time = clock();
	while (clock() < beginning_time + m_seconds);
}

int main()
{
	srand(time(NULL));

	const char* ip_address = "127.0.0.1";
	WSADATA data;

	// Initializing ws2_32.lib

	if (WSAStartup(MAKEWORD(2, 2), &data) != 0)
	{
		cerr << "ws2_32.lib error." << endl;
		system("pause");
		return 1;
	}

	// Creating the socket

	SOCKET accepted_socket = socket(AF_INET, SOCK_STREAM, 0);
	if (accepted_socket == INVALID_SOCKET)
	{
		cerr << "Socket creation failed. Error #" << WSAGetLastError() << endl;
		WSACleanup();
		system("pause");
		return 1;
	}

	// Creating an information structure

	sockaddr_in hint;
	hint.sin_family = AF_INET;
	hint.sin_port = htons(PORT);
	inet_pton(AF_INET, ip_address, &hint.sin_addr);

	// Connecting to the server
	
	if (connect(accepted_socket, (struct sockaddr*)&hint, sizeof(hint)) == INVALID_SOCKET)
	{
		cerr << "Socket connection failed. Error #" << WSAGetLastError() << endl;
		closesocket(accepted_socket);
		WSACleanup();
		system("pause");
		return 1;
	}

	// Receiving and processing the server's data

	char buffer[512] = { 0 };
	char u_input[65];

	delay(10);
	
	while (1) // бесконечный цикл, в котором передаем случайное число на сервер, а также ждем случайное количество времени от 0 до 10 секунд
	{
		intToStr(rand() % 100, u_input);
		int sending_back = send(accepted_socket, u_input, strlen(u_input) + 1, 0);
		if (sending_back != SOCKET_ERROR)
		{
			int received = recv(accepted_socket, buffer, 65, 0);
			if (received > 0)
			{
				cout << "ANOTHER_CLIENT>> " << string(buffer, 0, received) << endl;
			}
		}

		delay(rand() % 10); // ждем от 0 до 10 секунд (для простоты тестирования
	}

	closesocket(accepted_socket);
	WSACleanup();

	system("pause");
	return 0;
}


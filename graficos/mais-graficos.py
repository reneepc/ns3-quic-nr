#! /usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import sys
from statistics import mean

def plota_grafico(arquivo, num_apps):
    app = []
    number_of_packets = []
    data_size = []
    data_bit_rate = []
    average_packet_size = []
    average_packet_rate  = []
    different_ips = []
    

    with open(arquivo) as f:
        for i in range(num_apps):
            aplicativo = f.readline().split('/')[1].split('-')[0]
            print(aplicativo)
            if(aplicativo == 'googlePodcasts'):
                for i in range(9):
                    next(f)
                continue
            if(aplicativo == 'netflix'):
                for i in range(8):
                    next(f)
                continue
            app.append(aplicativo)
            n_packets = f.readline().split(':')[1].strip()[:-1]
            n_packets = ''.join(c for c in n_packets if c.isnumeric())
            number_of_packets.append(int(n_packets))

            d_size = f.readline().split(':')[1].strip()[:-2]
            d_size = ''.join(c for c in d_size if c.isnumeric())
            data_size.append(int(d_size))
            next(f)

            d_bit_rate = f.readline().split(':')[1].strip()[:-4]
            d_bit_rate = ''.join(c for c in d_bit_rate if c.isnumeric())
            if app[-1] == 'netflix':
                data_bit_rate.append(int(d_bit_rate) * 1000)
            else:
                data_bit_rate.append(int(d_bit_rate))

            avg_packet_size = f.readline().split(':')[1].strip()
            avg_packet_size = ''.join(c for c in avg_packet_size if c.isnumeric() or c == '.')
            average_packet_size.append(float(avg_packet_size))

            avg_packet_rate = f.readline().split(':')[1].strip()
            avg_packet_rate = ''.join(c for c in avg_packet_rate if c.isnumeric())
            average_packet_rate.append(int(avg_packet_rate))

            different_ips.append(int(f.readline().split(':')[1].strip()))
            try:
                if((line := f.readline()) != '\n'):
                    line = line.split(':')[1].strip()
                    different_ips[-1] = int(different_ips[-1]) + int(line)
                    next(f)
            except:
                print("Hey")
            print(app)
            print(different_ips);
        colors = ['royalblue', 'royalblue', 'slategray', 'royalblue', 'slategray', 'slategray', 'royalblue', 'royalblue']
        edgecolors = ['blue', 'blue', 'darkgray', 'blue', 'darkgray', 'darkgray', 'blue', 'blue']
        media = Rectangle((0, 0), 1, 1, fc="red", fill=True, edgecolor='red', linewidth=0)
        quic = Rectangle((0, 0), 1, 1, fc="blue", fill=True, edgecolor='red', linewidth=0)
        tcp = Rectangle((0, 0), 1, 1, fc="gray", fill=True, edgecolor='red', linewidth=0)

        ylabel_size = 14
        legend_size = 12
        title_size = 20
        label_size = 12
        tick_size = 12

        fig, ax = plt.subplots(3,2)
        ax[0][0].bar(app, number_of_packets, color = colors, edgecolor = edgecolors)
        ax[0][0].set_title("Número de Pacotes Trocados", fontsize=title_size)
        ax[0][0].set_ylabel("Milhares de pacotes", fontsize=ylabel_size)
        ax[0][0].axhline(mean(number_of_packets), color='red', linewidth=2)
        ax[0][0].legend([media, quic, tcp], ['Média: {:0.2f}'.format(mean(number_of_packets)), 'QUIC', 'TCP'],
                fontsize=legend_size);
        ax[0][0].yaxis.set_tick_params(labelsize=tick_size)
        ax[0][0].xaxis.set_tick_params(labelsize=tick_size)
        #plt.show()

        #fig, ax = plt.subplots(1,2)
        ax[0][1].bar(app, data_size, color = colors)
        ax[0][1].set_title("Número de Bytes Trocados", fontsize=title_size)
        ax[0][1].set_ylabel("Megabytes - MB", fontsize=ylabel_size)
        ax[0][1].axhline(mean(data_size), color='red', linewidth=2)
        ax[0][1].legend([media, quic, tcp], ['Média: {:0.2f}'.format(mean(data_size)), 'QUIC', 'TCP'],
                fontsize=legend_size);
        ax[0][1].yaxis.set_tick_params(labelsize=tick_size)
        ax[0][1].xaxis.set_tick_params(labelsize=tick_size)
        #plt.show()

        #fig, ax = plt.subplots()
        ax[1][0].bar(app, data_bit_rate, color = colors)
        ax[1][0].set_title("Taxa de Transferência", fontsize=title_size)
        ax[1][0].set_ylabel("Kilobits por segundo - kbps", fontsize=ylabel_size)
        ax[1][0].axhline(mean(data_bit_rate), color='red', linewidth=2)
        ax[1][0].legend([media, quic, tcp], ['Média: {:0.2f}'.format(mean(data_bit_rate)), 'QUIC', 'TCP'],
                fontsize=legend_size);
        ax[1][0].yaxis.set_tick_params(labelsize=tick_size)
        ax[1][0].xaxis.set_tick_params(labelsize=tick_size)
        #plt.show()

        #fig, ax = plt.subplots()
        ax[1][1].bar(app, average_packet_size, color = colors)
        ax[1][1].set_title("Média do Tamanho dos Pacotes", fontsize=title_size)
        ax[1][1].set_ylabel("Bytes", fontsize=ylabel_size)
        ax[1][1].axhline(mean(average_packet_size), color='red', linewidth=2)
        ax[1][1].legend([media, quic, tcp], ['Média: {:0.2f}'.format(mean(average_packet_size)), 'QUIC', 'TCP'],
                fontsize=legend_size);
        ax[1][1].yaxis.set_tick_params(labelsize=tick_size)
        ax[1][1].xaxis.set_tick_params(labelsize=tick_size)
        #plt.show()

        #fig, ax = plt.subplots()
        ax[2][0].bar(app, average_packet_rate, color = colors)
        ax[2][0].set_title("Média da Taxa de Pacotes", fontsize=title_size)
        ax[2][0].set_ylabel("Pacotes por Segundo", fontsize=ylabel_size)
        ax[2][0].axhline(mean(average_packet_rate), color='red', linewidth=2)
        ax[2][0].legend([media, quic, tcp], ['Média: {:0.2f}'.format(mean(average_packet_rate)), 'QUIC', 'TCP'],
                fontsize=legend_size);
        ax[2][0].yaxis.set_tick_params(labelsize=tick_size)
        ax[2][0].xaxis.set_tick_params(labelsize=tick_size)
        #plt.show()
        plt.xticks(rotation=45, ha="right")

        #fig, ax = plt.subplots()
        ax[2][1].bar(app, different_ips, color = colors)
        ax[2][1].set_title("Número de endereços IP diferentes", fontsize=title_size)
        ax[2][1].set_ylabel("Número de endereços", fontsize=ylabel_size)
        ax[2][1].axhline(mean(different_ips), color='red', linewidth=2)
        ax[2][1].legend([media, quic, tcp], ['Média: {:0.2f}'.format(mean(different_ips)), 'QUIC', 'TCP'],
                fontsize=legend_size) 
        ax[2][1].yaxis.set_tick_params(labelsize=tick_size)
        ax[2][1].xaxis.set_tick_params(labelsize=tick_size)

        plt.tight_layout()
        for i in range(3):
            for j in range(2):
                plt.setp(ax[i][j].xaxis.get_majorticklabels(), rotation=45)
        plt.savefig('general-stats-fonte.png', bbox_inches='tight');
        plt.show()

if __name__ == '__main__':
    plota_grafico("pcap-general-stats.txt", 10);

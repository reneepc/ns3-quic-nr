// Passos fundamentais:
//
// Configurar o canal que será associado a um dispositivo de rede.
// phy é a camada física que utiliza o canal. O que manda e recebe sinais.
// Configurar mac (decidir a arquitetura)
// Configurar o dispositivo, em especial o padrão 802.11
// MOBILIDADE, mesmo que os dispositivos sejam estacionários
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/wifi-module.h"
#include "ns3/mobility-module.h"
#include "ns3/applications-module.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE("WifiTest");

int main(int argc, char* argv[]) {

    LogComponentEnable("UdpEchoClientApplication", LOG_LEVEL_INFO);
    LogComponentEnable("UdpEchoServerApplication", LOG_LEVEL_INFO);
    //LogComponentEnableAll(LOG_PREFIX_ALL);

    NodeContainer staNodes;
    staNodes.Create(4);
    NodeContainer apNodes;
    apNodes.Create(1);

    // Especialmente Modelo de latencia e perda (delay e loss)
    YansWifiChannelHelper channel = YansWifiChannelHelper::Default();

    // Phy sao os dispositivos físicos, incluindo um modelo para os erros
    // ErroRateModel.
    YansWifiPhyHelper phy;
    phy.SetErrorRateModel("ns3::NistErrorRateModel");
    phy.SetChannel(channel.Create());
    phy.Set("Antennas", UintegerValue(2));
    phy.Set("MaxSupportedTxSpatialStreams", UintegerValue(2));
    phy.Set("MaxSupportedRxSpatialStreams", UintegerValue(2));

    // Decide a função do dispositivo na rede (Ponto de acesso, estação ou
    // ad-hoc).
    WifiMacHelper mac;

    WifiHelper wifi;
    wifi.SetStandard(WIFI_STANDARD_80211ax_5GHZ);
    wifi.SetRemoteStationManager("ns3::ConstantRateWifiManager");

    NetDeviceContainer wifiStaDevices;
    NetDeviceContainer wifiApDevices;

    mac.SetType("ns3::StaWifiMac");
    wifiStaDevices = wifi.Install(phy, mac, staNodes);
    mac.SetType("ns3::ApWifiMac");
    wifiApDevices = wifi.Install(phy, mac, apNodes);

    MobilityHelper mobility;
    Ptr<ListPositionAllocator> positions = CreateObject<ListPositionAllocator>();
    positions->Add(Vector(0.0,0.0,0.0));
    positions->Add(Vector(5.0,0.0,0.0));
    positions->Add(Vector(0.0,5.0,0.0));
    mobility.SetPositionAllocator(positions);
    mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
    mobility.Install(apNodes);
    mobility.Install(staNodes);

    // NS_LOG_INFO("Assign IPv4 Addresses")
    InternetStackHelper IntHelper;
    IntHelper.Install(apNodes);
    IntHelper.Install(staNodes);

    Ipv4AddressHelper ipv4;
    ipv4.SetBase("192.168.1.0", "255.255.255.0");
    Ipv4InterfaceContainer icap = ipv4.Assign(wifiApDevices);
    Ipv4InterfaceContainer icsta = ipv4.Assign(wifiStaDevices);

    int16_t port = 50000;
    UdpEchoServerHelper echoServer(port);
    ApplicationContainer serverApps = echoServer.Install(apNodes);
    serverApps.Start(Seconds(1.0));
    serverApps.Stop(Seconds(10.0));

    UdpEchoClientHelper echoClient(icap.GetAddress(0), port);
    echoClient.SetAttribute("MaxPackets", UintegerValue(3));
    echoClient.SetAttribute("Interval", TimeValue(Seconds(1)));
    echoClient.SetAttribute("PacketSize", UintegerValue(1024));

    ApplicationContainer clientApps = echoClient.Install(staNodes);
    clientApps.Start(Seconds(2.0));
    clientApps.Stop(Seconds(10.0));

    Simulator::Stop(Seconds(10.0));
    Simulator::Run();
    Simulator::Destroy();

    return 0;
}

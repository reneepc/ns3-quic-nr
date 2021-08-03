/*
 * This script simulates a simple network in which one end device sends one
 * packet to the gateway.
 */

#include "ns3/end-device-lora-phy.h"
#include "ns3/gateway-lora-phy.h"
#include "ns3/end-device-lorawan-mac.h"
#include "ns3/gateway-lorawan-mac.h"
#include "ns3/simulator.h"
#include "ns3/log.h"
#include "ns3/constant-position-mobility-model.h"
#include "ns3/lora-helper.h"
#include "ns3/mobility-helper.h"
#include "ns3/node-container.h"
#include "ns3/position-allocator.h"
#include "ns3/one-shot-sender-helper.h"
#include "ns3/command-line.h"
#include <algorithm>
#include <ctime>
#include <cmath>

using namespace ns3;
using namespace lorawan;

NS_LOG_COMPONENT_DEFINE ("SimpleLorawanNetworkExample");

MobilityHelper GridAllocator(int nNodes) {
  MobilityHelper mobility;
  Ptr<ListPositionAllocator> allocator = CreateObject<ListPositionAllocator> ();

  int colunas = ceil(sqrt(nNodes));
  for(int i = 0; i < nNodes; i++) {
    allocator->Add(Vector((i%colunas)*1000, i/colunas, 0));
  }

  mobility.SetPositionAllocator (allocator);
  mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
  return mobility;
}


int main (int argc, char *argv[])
{

  // Set up logging
  LogComponentEnable ("SimpleLorawanNetworkExample", LOG_LEVEL_ALL);
  LogComponentEnable ("LoraChannel", LOG_LEVEL_INFO);
  LogComponentEnable ("LoraPhy", LOG_LEVEL_ALL);
  LogComponentEnable ("EndDeviceLoraPhy", LOG_LEVEL_ALL);
  LogComponentEnable ("GatewayLoraPhy", LOG_LEVEL_ALL);
  //LogComponentEnable ("LoraInterferenceHelper", LOG_LEVEL_ALL);
  //LogComponentEnable ("LorawanMac", LOG_LEVEL_ALL);
  //LogComponentEnable ("EndDeviceLorawanMac", LOG_LEVEL_ALL);
  //LogComponentEnable ("ClassAEndDeviceLorawanMac", LOG_LEVEL_ALL);
  //LogComponentEnable ("GatewayLorawanMac", LOG_LEVEL_ALL);
  //LogComponentEnable ("LogicalLoraChannelHelper", LOG_LEVEL_ALL);
  //LogComponentEnable ("LogicalLoraChannel", LOG_LEVEL_ALL);
  //LogComponentEnable ("LoraHelper", LOG_LEVEL_ALL);
  //LogComponentEnable ("LoraPhyHelper", LOG_LEVEL_ALL);
  //LogComponentEnable ("LorawanMacHelper", LOG_LEVEL_ALL);
  //LogComponentEnable ("OneShotSenderHelper", LOG_LEVEL_ALL);
  //LogComponentEnable ("OneShotSender", LOG_LEVEL_ALL);
  //LogComponentEnable ("LorawanMacHeader", LOG_LEVEL_ALL);
  //LogComponentEnable ("LoraFrameHeader", LOG_LEVEL_ALL);
  LogComponentEnableAll (LOG_PREFIX_FUNC);
  LogComponentEnableAll (LOG_PREFIX_NODE);
  LogComponentEnableAll (LOG_PREFIX_TIME);

  /************************
  *  Create the channel  *
  ************************/

  // First, the channel will be create, which needs a loss model and a delay model.
  NS_LOG_INFO ("Creating the channel...");

  // Create the lora channel object
  Ptr<LogDistancePropagationLossModel> loss = CreateObject<LogDistancePropagationLossModel> ();
  loss->SetPathLossExponent (3.76);
  loss->SetReference (1, 7.7);

  Ptr<PropagationDelayModel> delay = CreateObject<ConstantSpeedPropagationDelayModel> ();

  // The channel could be created only by instantiating the LoraChannel object passing the two models.
  Ptr<LoraChannel> channel = CreateObject<LoraChannel> (loss, delay);

  /************************
  *  Create the helpers  *
  ************************/

  NS_LOG_INFO ("Setting up helpers...");

  // Second, there must be a mobility allocator and a mobility model.
  MobilityHelper mobility = GridAllocator(2);
  //Ptr<ListPositionAllocator> allocator = CreateObject<ListPositionAllocator> ();
  //allocator->Add (Vector (1000,0,0));
  //allocator->Add (Vector (0,0,0));
  //mobility.SetPositionAllocator (allocator);
  //mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");

  // Create the LoraPhyHelper
  LoraPhyHelper phyHelper = LoraPhyHelper ();
  phyHelper.SetChannel (channel);

  // Create the LorawanMacHelper
  LorawanMacHelper macHelper = LorawanMacHelper ();

  // Create the LoraHelper
  LoraHelper helper = LoraHelper ();

  /************************
  *  Create End Devices  *
  ************************/

  NS_LOG_INFO ("Creating the end device...");

  // Create a set of nodes
  NodeContainer endDevices;
  endDevices.Create (1);

  // Assign a mobility model to the node
  mobility.Install (endDevices);

  // Create the LoraNetDevices of the end devices
  phyHelper.SetDeviceType (LoraPhyHelper::ED);
  macHelper.SetDeviceType (LorawanMacHelper::ED_A);
  helper.Install (phyHelper, macHelper, endDevices);

  /*********************
  *  Create Gateways  *
  *********************/

  NS_LOG_INFO ("Creating the gateway...");
  NodeContainer gateways;
  gateways.Create (1);

  mobility.Install (gateways);

  // Create a netdevice for each gateway
  phyHelper.SetDeviceType (LoraPhyHelper::GW);
  macHelper.SetDeviceType (LorawanMacHelper::GW);
  helper.Install (phyHelper, macHelper, gateways);

  /*********************************************
  *  Install applications on the end devices  *
  *********************************************/

  OneShotSenderHelper oneShotSenderHelper;
  oneShotSenderHelper.SetSendTime (Seconds (2));

  oneShotSenderHelper.Install (endDevices);

  /******************
   * Set Data Rates *
   ******************/
  std::vector<int> sfQuantity (6);
  sfQuantity = macHelper.SetSpreadingFactorsUp (endDevices, gateways, channel);

  /****************
  *  Simulation  *
  ****************/

  Simulator::Stop (Hours (2));

  Simulator::Run ();

  Simulator::Destroy ();

  return 0;
}

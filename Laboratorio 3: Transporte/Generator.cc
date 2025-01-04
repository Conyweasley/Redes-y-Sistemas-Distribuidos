#ifndef GENERATOR
#define GENERATOR

#include <string.h>
#include <omnetpp.h>

using namespace omnetpp;

class Generator : public cSimpleModule {
private:
    cMessage *sendMsgEvent;
    cStdDev transmissionStats;
    cOutVector pSendVector;
    unsigned int counter;
public:
    Generator();
    virtual ~Generator();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};
Define_Module(Generator);

Generator::Generator() {
    sendMsgEvent = NULL;

}

Generator::~Generator() {
    cancelAndDelete(sendMsgEvent);
}

void Generator::initialize() {
    transmissionStats.setName("TotalTransmissions");
    pSendVector.setName("PaquetesEnviados");
    counter = 0u;
    // create the send packet
    sendMsgEvent = new cMessage("sendEvent");
    // schedule the first event at random time
    scheduleAt(par("generationInterval"), sendMsgEvent);
}

void Generator::finish() {
}

void Generator::handleMessage(cMessage *msg) {

    // create new packet
    cPacket *pkt;
    pkt = new cPacket("packet");
    pkt->setByteLength(par("packetByteSize"));
    // send to the output
    send(pkt, "out");
    counter++;
    // compute the new departure time
    simtime_t departureTime = simTime() + par("generationInterval");
    pSendVector.record(counter);
    // schedule the new packet generation
    scheduleAt(departureTime, sendMsgEvent);
}

#endif /* GENERATOR */

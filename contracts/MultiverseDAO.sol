// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MultiverseDAO {
    struct Proposal {
        string title;
        uint256 yes;
        uint256 no;
        bool executed;
    }

    mapping(uint256 => Proposal) public proposals;
    mapping(uint256 => mapping(address => bool)) public voted;
    uint256 public proposalCount;

    event Proposed(uint256 indexed id, string title);
    event Voted(uint256 indexed id, address voter, bool support);
    event Executed(uint256 indexed id, bool approved);

    function propose(string calldata title) external returns (uint256 id) {
        id = ++proposalCount;
        proposals[id] = Proposal(title, 0, 0, false);
        emit Proposed(id, title);
    }

    function vote(uint256 id, bool support) external {
        require(id > 0 && id <= proposalCount, "bad id");
        require(!voted[id][msg.sender], "already voted");
        require(!proposals[id].executed, "executed");
        voted[id][msg.sender] = true;
        if (support) proposals[id].yes += 1;
        else proposals[id].no += 1;
        emit Voted(id, msg.sender, support);
    }

    function execute(uint256 id) external returns (bool approved) {
        require(id > 0 && id <= proposalCount, "bad id");
        Proposal storage p = proposals[id];
        require(!p.executed, "executed");
        p.executed = true;
        approved = p.yes >= p.no;
        emit Executed(id, approved);
    }
}

